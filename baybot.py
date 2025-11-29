import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()  # Carga las variables del archivo .env

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.CustomActivity(
            "/help · baybot.gg · discord.gg/baybot"
        )
    )
    print(f"Bot iniciado como {bot.user}")


bot.run(TOKEN)
