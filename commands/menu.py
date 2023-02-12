from config import bot_dm, bot_general, bot_menu, bot_menu_removal
from utils.delete_all_user import delete_all_user_messages
from utils.get_menu_text import get_menu_text
import discord
import time

# Time since command was used
last_menu_time = 0

async def menu(message, client): 

    # Time since command was used
    global last_menu_time

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
        await delete_all_user_messages(message.channel, client.user.id, bot_menu) # TODO fix temp solv
        await delete_all_user_messages(message.channel, client.user.id, bot_menu_removal)
        menu_text = await get_menu_text()
        await message.channel.send(menu_text)
        await message.delete()
    except discord.errors.HTTPException as e:
        if e.status == 400:
            print(f'An error occurred: {e}')
            bot_message = await message.channel.send(bot_menu)
            await bot_message.delete(delay=60)
            await message.delete()
        elif e.status == 403:
            print(f'An error occurred: {e}')
            bot_message = await message.channel.send(bot_dm)
            await bot_message.delete(delay=60)
            await message.delete()
        elif e.status:
            print(f'An error occurred: {e}')
            bot_message = await message.channel.send(bot_general)
            await bot_message.delete(delay=60)
            await message.delete()