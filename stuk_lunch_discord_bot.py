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
url_stuk = "https://www.stuk.nu/"

url_stuk_div = '//div[@class="w-restaurant-menu"]'

# Alternativ url for the restiramt's menu page
url_matochmat = "https://www.matochmat.se/lunch/lulea/stuk/"

url_matochmat_div = '//div[@class="lunchMenuDetailsDay"]'

# Time since command was used
last_menu_time = 0

# List of available commands
commands = {
    "   **!menu**": "`Displays the restaurant's menu`",
    "   **!help**": "`Lists all the commands the bot has`",
    "   **!url**": "`shows the url from which the menu was taken`",
}

# Format the menu text
async def get_menu_text():
    try:
        # source of the url
        source = url_stuk
        # create an AsyncHTMLSession object
        asession = AsyncHTMLSession()
        # use the object to send a GET request to the menu page
        r = await asession.get(url_stuk)
        # wait for the page to load
        await r.html.arender()
        # find all elements with the class "w-restaurant-menu"
        menu = r.html.xpath(url_stuk_div, first=False)

        # If theres not a menu on the stuk url, try this one
        if len(menu) == 0:  # if menu is empty
            # source of the url
            source = url_matochmat
            # create an AsyncHTMLSession object
            r = await asession.get(url_matochmat)
            # wait for the page to load
            await r.html.arender()
            # find all elements with the class "w-restaurant-menu"
            menu = r.html.xpath(url_matochmat_div, first=False)

        # A list of all menu items and dates in text form
        itemlist = []

        # Extract text from menu elements and clean it up
        for item in menu:
            itemlist.append(item.text)

        # Formatting the list
        cleaned_list = [re.sub(r"(\d+ kr|\nkr)", "", item)
                        for item in itemlist if "Lördag" not in item and "Söndag" not in item]
        cleaned_list = [re.sub(r"\n105\xa0kr\n", " ", item)
                        for item in cleaned_list]  # for the matchomat menu
        cleaned_list = [re.sub(r"\nmed", " ", item)
                        for item in cleaned_list]  # for the matchomat menu
        cleaned_list = [re.sub(r"\n\n", " ", item) for item in cleaned_list]
        cleaned_list = [re.sub(r"(\n)$", "", item) for item in cleaned_list]
        cleaned_list = [re.sub(r"\n\n", " ", item) for item in cleaned_list]
        cleaned_list = [re.sub(r"\n([a-z])", r" \1", item)
                        for item in cleaned_list]

        formatted_menu = ""
        for item in cleaned_list:
            day = item.split("\n")[0]
            meals = item.split("\n")[1:]
            formatted_menu += "\n**" + day + "**\n"
            for meal in meals:
                formatted_menu += "• " + meal + "\n"

        if len(formatted_menu) == 0:
            formatted_menu = "\n**The menu has not yet been uploaded, try again later **"
        formatted_menu = "\n**Stuk Lunch Menu:  **\n\n**  Source**: <" + \
            source + ">\n" + formatted_menu
        return formatted_menu

    except Exception as e:
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
    print(f"Username: {message.author.name} \nID: {message.author.id} \nCommand: {message.content}  ")

    # figure out a way to delete previous menu posting
    if message.content.startswith("!menu"):
        try:
            # check if the command was used within the last 30 seconds
            current_time = time.time()
            time_since_last = current_time - last_menu_time
            if time_since_last < 30:
                remaining_time = round(30 - time_since_last)
                bot_message = await message.channel.send(f"Please wait {remaining_time} seconds before using the command again.")
                await bot_message.delete(delay=60)
                await message.delete()
                return
            last_menu_time = current_time
            await delete_all_user_messages(message.channel, client.user.id, "Stuk Lunch Menu:")
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
            help_text = "**Available commands:**\n"
            for command, description in commands.items():
                help_text += f"{command}: {description}\n"
            bot_message = await message.channel.send(help_text)
            await bot_message.delete(delay=60)  # delete after 1 minutesw
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
            bot_message = await message.channel.send(f"The menu's source is: <{url_stuk}> or <{url_matochmat}>")
            await bot_message.delete(delay=60)  # delete after 1 minutes
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
            await bot_message.delete(delay=60)  # delete after 1 minutes
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
