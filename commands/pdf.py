from config import base_url, restaurant, pdf_type, pdf_bol
from utils.delete_all_user import delete_all_user_files
from utils.build_url import build_url
from pdf2jpg import pdf2jpg
import requests
import discord

async def pdf(message, client):
    try:
        await delete_all_user_files(message.channel, client.user.id)
        url = build_url(base_url, restaurant, pdf_type, pdf_bol)
        response = requests.get(url)
        open("pdf_file.pdf", "wb").write(response.content)
        inputpath = r"pdf_file.pdf"
        outputpath = r""
        pdf2jpg.convert_pdf2jpg(inputpath,outputpath, pages="ALL")
        await message.channel.send(file=discord.File("./pdf_file.pdf_dir/0_pdf_file.pdf.jpg"))
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