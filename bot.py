from commands.menu import menu
from commands.help import help
from commands.pdf import pdf
from commands.url import url
from dotenv import load_dotenv
import discord
import os

# loads the .env file
load_dotenv()

client = discord.Client(intents=discord.Intents.all())

# Tells when bot is ready
@client.event
async def on_ready():
    print('Bot is ready.')

# Discord bot command to show menu
@client.event
async def on_message(message):

    # Makes it so the bot does not check anything if the command does not have !
    if not message.content.startswith('!'):
        return

    # print the username and ID of the user who sent the message
    print(f'Username: {message.author.name} \nID: {message.author.id} \nCommand: {message.content}  ')

    if message.content.startswith('!menu'):
       await menu(message, client)

    elif message.content.startswith('!pdf'):
        await pdf(message,client)

    elif message.content.startswith('!help'):
        await help(message)

    elif message.content.startswith('!url'):
        await url(message)

    else: #invalid command
        bot_message = await message.channel.send('Invalid command. Please use `!help` to see a list of valid commands.')
        await bot_message.delete(delay=60)  # delete after 1 minutes
        await message.delete()

# Run the bot
client.run(os.getenv('SECRET_KEY_DISCORD'))
