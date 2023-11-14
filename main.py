import AIchat
import discord
import os

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('起動しました')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user.mentioned_in(message):
      await message.channel.send(AIchat.chatfireworks(message.clean_content.replace('@radianのbot test', '')))

TOKEN = os.getenv("Discord_token")
client.run(TOKEN)
