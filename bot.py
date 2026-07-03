"""Main Bot file"""

from sys import exit as sysexit
import subprocess
import json
import argparse
import time
import asyncio
import discord
from discord.ext import commands
from color_logger.color_logger import create_logger, DEBUG, INFO, ColorFormatter
from utils.scheduler import start_scheduler

parser = argparse.ArgumentParser()
parser.add_argument(
    "--debug", action="store_true", required=False, help="Use this to enter Debug mode"
)
parser.add_argument(
    "--update-bot",
    action="store_true",
    required=False,
    help="Use this to clear commands for all servers",
)
parser.add_help = True
args = parser.parse_args()
log = create_logger("FootBot", True, DEBUG if args.debug is True else INFO)

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
    await bot.load_extension("cogs.config")
    await bot.load_extension("cogs.roster")
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.view")
    await bot.load_extension("cogs.leaderboard")
    await bot.load_extension("cogs.map")
    await bot.load_extension("cogs.submit")

@bot.event
async def on_ready() -> None:
    """Starts scheduler"""
    if args.update_bot:
        bot.tree.clear_commands(guild=None, type=None)
        for guild in bot.guilds:
            bot.tree.clear_commands(guild=guild, type=None)
            log.debug("Guild %s has been cleared.", guild)
        subprocess.Popen(
            "python C:/Users/kolay/FootBot/bot.py" + " --debug" if args.debug else "",
            shell=True,
            start_new_session=True,
        )
        time.sleep(2)
        sysexit(0)
    await bot.tree.sync()
    log.info("✅ Logged in as %s", bot.user)
    start_scheduler(bot)


TOKEN = secrets["DISCORD_TOKEN"]
if isinstance(TOKEN, int):
    raise TypeError("Rejected type int: This value must be a str")
if __name__ == "__main__":
    try:
        time.sleep(5)
        asyncio.run(setup())
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
        loop.run_until_complete(bot.close())
