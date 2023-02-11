import discord
from config import url_stuk, url_matochmat

async def url(message):
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