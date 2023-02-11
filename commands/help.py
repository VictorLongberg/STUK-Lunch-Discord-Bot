from config import commands
import discord

async def help(message):
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