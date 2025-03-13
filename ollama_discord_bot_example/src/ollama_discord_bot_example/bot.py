import discord
from ollama import Client, AsyncClient

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ai'):
        response = await AsyncClient(
            host='http://ollama:11434'
        ).chat(model='tinyllama:1.1b-chat-v0.6-q2_K', messages=[
            {
                'role': 'user',
                'content': 'Why is the sky blue?',
            },
        ])
        await message.channel.send(response.message.content)

def start():
    client.run('')