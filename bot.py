import asyncio
import discord
from discord.ext import commands
from utils.scheduler import start_scheduler

intents: discord.Intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

async def setup() -> None:
    """Prepares the bot"""
    await bot.load_extension("cogs.config")
    await bot.load_extension("cogs.roster")
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.view")

@bot.event
async def on_ready() -> None:
    """Starts scheduler"""
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")
    start_scheduler(bot)

if __name__ == "__main__":
    asyncio.run(setup())
    bot.run("YOUR_TOKEN_HERE")
