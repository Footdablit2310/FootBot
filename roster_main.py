"""Roster bot main file"""

import os
from sys import exit as sysexit, path
import json
import time
import asyncio
import discord
from discord.ext import commands
from color_logger.color_logger import create_logger, DEBUG, INFO, ColorFormatter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in path:
    path.insert(0, PROJECT_ROOT)
# pylint: disable=C0413, E0611
from runner.run_bot import args, SECRETS_PATH

log = create_logger("FootRosterBot", True, DEBUG if args.debug is True else INFO)
with open(SECRETS_PATH, "r", encoding="utf-8") as f:
    secrets: dict[str, int | str] = json.load(f)
TOKEN = str(secrets["ROSTER_TOKEN"])

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

async def setup() -> None:
    """Prepares the bot"""
    await bot.load_extension("cogs.config")
    await bot.load_extension("cogs.roster")
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.view")

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
        sysexit(503)
    await bot.tree.sync()

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
