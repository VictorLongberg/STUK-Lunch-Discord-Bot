# function to delete previous menu posts
async def delete_all_user_messages(channel, user_id, phrase):
    async for message in channel.history(limit=None):
        if message.author.id == user_id and phrase in message.content:
            await message.delete()

# function to delete previous file posts
async def delete_all_user_files(channel, user_id):
    async for message in channel.history(limit=None):
        if message.attachments and message.author.id == user_id:
            await message.delete()