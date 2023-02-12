from config import url_stuk, url_matochmat, bot_dm, bot_general
import discord

async def url(message):
    try:
        # send the source url of the menu
        bot_message = await message.channel.send(f"The menu's source is: <{url_stuk}> or <{url_matochmat}>")
        await bot_message.delete(delay=60)  # delete after 1 minutes
        await message.delete()
    except discord.errors.HTTPException as e:
        if e.status == 403:
            print(f'An error occurred: {e}')
            bot_message = await message.channel.send(bot_dm)
            await bot_message.delete(delay=60)
            await message.delete()
        elif e.status:
            print(f'An error occurred: {e}')
            bot_message = await message.channel.send(bot_general)
            await bot_message.delete(delay=60)
            await message.delete()