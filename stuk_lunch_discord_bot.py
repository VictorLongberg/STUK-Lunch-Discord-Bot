from requests_html import AsyncHTMLSession
from dotenv import load_dotenv
import discord
import time
import re
import os

# loads the .env file
load_dotenv()

client = discord.Client(intents=discord.Intents.all())

# URL for the restaurant's menu page
url = "https://www.stuk.nu/"

# Time since command was used
last_menu_time = 0

# List of available commands
commands = {
    "   !menu": "`Displays the restaurant's menu`",
    "   !help": "`Lists all the commands the bot has`",
    "   !url": "`shows the url from which the menu was taken`"
}

# format the menu text
async def get_menu_text():
    try:
        # create an AsyncHTMLSession object
        asession = AsyncHTMLSession()
        # use the object to send a GET request to the menu page
        r = await asession.get(url)
        # wait for the page to load
        await r.html.arender()
        # find all elements with the class "w-restaurant-menu"
        menu = r.html.xpath('//div[@class="w-restaurant-menu"]', first=False)

        # A list of all menu items and dates in text form
        itemlist = []

        # Extract text from menu elements and clean it up
        for item in menu:
            itemlist.append(item.text)

        cleaned_list = [re.sub(r"(\d+ kr|\nkr)", "", item) for item in itemlist if "Lördag" not in item and "Söndag" not in item]
        cleaned_list = [re.sub(r"\n\n", " ", item) for item in cleaned_list]
        cleaned_list = [re.sub(r"(\n)$", "", item) for item in cleaned_list]

        formatted_menu = ""
        for item in cleaned_list:
            day = item.split("\n")[0]
            meals = item.split("\n")[1:]
            formatted_menu += "\n**" + day + "**\n"
            for meal in meals:
                formatted_menu += "• " + meal + "\n"

        formatted_menu = "\n**Stuk Lunch Meny:  **\n" + formatted_menu

        return formatted_menu

    except Exception as e:
        # print the error message
        print(f'An error occurred: {e}')
        return 'Sorry, an error occurred while trying to fetch the menu.'


# function to delete previous menu post
async def delete_all_user_messages(channel, user_id, phrase):
    async for message in channel.history(limit=None):
        if message.author.id == user_id and phrase in message.content:
            await message.delete()


# Discord bot command to show menu
@client.event
async def on_message(message):

    # Makes it so the bot does not check anything if the command does not have !
    if not message.content.startswith("!"):
        return

    # Time since command was used
    global last_menu_time

    # print the username and ID of the user who sent the message
    print("Username: ", message.author.name)
    print("ID: ", message.author.id)
    print("Command: ", message.content)

    if message.content.startswith("!menu"): #figure out a way to delete previous menu posting
        try:
            # check if the command was used within the last 30 seconds
            current_time = time.time()
            time_since_last = current_time - last_menu_time
            if time_since_last < 30:
                remaining_time = round(30 - time_since_last)
                await message.channel.send(f"Please wait {remaining_time} seconds before using the command again.")
                return
            last_menu_time = current_time

            await delete_all_user_messages(message.channel, client.user.id, "Stuk Lunch Meny:")
            
            menu_text = await get_menu_text()
            await message.channel.send(menu_text)
            await message.delete()

        except discord.errors.HTTPException as e:
            if e.status == 400:
                print(f'An error occurred: {e}')
                bot_message = await message.channel.send(' `\nSorry, an error occurred while trying to fetch the data, try again later`')
                await bot_message.delete(delay=60)
                await message.delete()
            elif e.status == 403:
                print(f'An error occurred: {e}')
                bot_message = await message.channel.send(' `\nSorry, the bot cannot remove commands sent directly to the bot`')
                await bot_message.delete(delay=60)
                await message.delete()

    elif message.content.startswith("!help"):
        try:
            help_text = "Available commands:\n"
            for command, description in commands.items():
                help_text += f"{command}: {description}\n"
            bot_message = await message.channel.send(help_text)
            await bot_message.delete(delay=60) # delete after 1 minutes
            await message.delete()
        except discord.errors.HTTPException as e:
            if e.status == 403:
                print(f'An error occurred: {e}')
                bot_message = await message.channel.send(' `\nSorry, the bot cannot remove commands sent directly to the bot`')
                await bot_message.delete(delay=60)
                await message.delete()
            elif e.status:
                print(f'An error occurred: {e}')
                bot_message = await message.channel.send('`\nAn unexpected Error Occured`')
                await bot_message.delete(delay=60)
                await message.delete() 

    elif message.content.startswith("!url"):
        try:
            # send the source url of the menu
            bot_message = await message.channel.send(f"The menu's source is: {url}")
            await bot_message.delete(delay=60) # delete after 1 minutes
            await message.delete()
        except discord.errors.HTTPException as e:
            if e.status == 403:
                print(f'An error occurred: {e}')
                bot_message = await message.channel.send(' `\nSorry, the bot cannot remove commands sent directly to the bot`')
                await bot_message.delete(delay=60)
                await message.delete()
            elif e.status:
                print(f'An error occurred: {e}')
                bot_message = await message.channel.send('`\nAn unexpected Error Occured`')
                await bot_message.delete(delay=60)
                await message.delete() 

    elif message.content.startswith("!"):
        try:
            bot_message = await message.channel.send("Invalid command. Please use `!help` to see a list of valid commands.")
            await bot_message.delete(delay=60) # delete after 1 minutes
            await message.delete()
        except discord.errors.HTTPException as e:
            if e.status == 403:
                print(f'An error occurred: {e}')
                bot_message = await message.channel.send(' `\nSorry, the bot cannot remove commands sent directly to the bot`')
                await bot_message.delete(delay=60)
                await message.delete()
            elif e.status:
                print(f'An error occurred: {e}')
                bot_message = await message.channel.send('`\nAn unexpected Error Occured`')
                await bot_message.delete(delay=60)
                await message.delete()  

# Run the bot
client.run(os.getenv('SECRET_KEY_DISCORD'))
