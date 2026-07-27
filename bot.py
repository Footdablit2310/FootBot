"""Main Bot file"""

from sys import exit as sysexit
import json
import time
import asyncio
import discord
from discord.ext import commands
from color_logger.color_logger import create_logger, DEBUG, INFO, ColorFormatter
from utils.storage import print_command_list
from runner.run_bot import args

log = create_logger("FootBot", True, DEBUG if args.debug is True else INFO)
log.debug("Initilized logger")
intents: discord.Intents = discord.Intents.default()

# Core guild and member access
intents.guilds = True
intents.members = True

# Needed for reading message content (warnings otherwise)
intents.message_content = True

# Optional but useful for event and role management
intents.guild_scheduled_events = True
intents.guild_messages = True
intents.guild_reactions = True

bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

with open("secrets.json", "r", encoding="utf-8") as f:
    secrets: dict[str, int | str] = json.load(f)

async def setup() -> None:
    """Prepares the bot"""
    await bot.load_extension("setup_bot")


@bot.event
async def on_ready() -> None:
    """Starts scheduler"""
    if args.update_bot:
        bot.status = discord.Status.offline
        bot.tree.clear_commands(guild=None, type=None)
        for guild in bot.guilds:
            bot.tree.clear_commands(guild=guild, type=None)
            log.debug("Guild %s has been cleared.", guild)
        time.sleep(3)
        bot.status = discord.Status.offline
        sysexit(0)
    await bot.tree.sync()
    print_command_list(log)


TOKEN = secrets["MAIN_TOKEN"]
if isinstance(TOKEN, int):
    raise TypeError("Rejected type int: This value must be a str")
if __name__ == "__main__":
    try:
        time.sleep(5)
        asyncio.run(setup())
        bot.status = discord.Status.online
        bot.run(
            TOKEN,
            log_handler=log.handlers[0],
            log_formatter=ColorFormatter(),
            log_level=DEBUG if args.debug is True else INFO,
            root_logger=False,
            reconnect=False,
        )
    except KeyboardInterrupt:
        loop = asyncio.get_event_loop()
        bot.status = discord.Status.invisible
        loop.run_until_complete(bot.close())
