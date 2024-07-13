import discord
from discord.ext import commands, tasks
import asyncio

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)

status_cycle = [discord.Status.online, discord.Status.idle, discord.Status.dnd, discord.Status.invisible]
change_status_task = None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

async def change_status():
    while True:
        for status in status_cycle:
            await bot.change_presence(status=status)
            await asyncio.sleep(5)  

@bot.event
async def on_message(message):
    global change_status_task

    if message.author == bot.user:
        return

    if message.content == '+':
        if change_status_task is None:
            change_status_task = bot.loop.create_task(change_status())
            await message.channel.send('Bot will now change status every 5 seconds.')
#upd
    elif message.content == '-':
        if change_status_task is not None:
            change_status_task.cancel()
            change_status_task = None
            await message.channel.send('Bot has stopped changing status.')
bot.run("")
