"""The setup file"""
from typing import Any, Dict

import discord
from discord import app_commands
from discord.ext import commands

from utils.storage import load_mc, save_mc, get_guild_data_mc, command_list_add
from utils.validator import validate_interaction_guild, check_for_guild_data


class SetupMC(commands.Cog):
    """The setup class for setting up the minecraft part"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setup-mc", description="Configure RCON for this guild")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_mc(
        self, interaction: discord.Interaction, host: str, port: int, password: str
    ) -> None:
        """Setup MC"""
        MC_FILE = "mc.json"
        guild = validate_interaction_guild(interaction)
        if check_for_guild_data(MC_FILE, guild):
            await interaction.response.send_message("Guild data already exists!")
            return None
        data: Dict[str, Any] = load_mc()
        guild_data = get_guild_data_mc(guild)

        guild_data["rcon"]["host"] = host
        guild_data["rcon"]["port"] = port
        guild_data["rcon"]["password"] = password

        data[str(guild.id)] = guild_data
        save_mc(data)

        await interaction.response.send_message(
            f"✅ RCON configured for this guild:\nHost: `{host}`\nPort: `{port}`",
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    """Prepares the bot"""
    command_list_add(SetupMC.setup_mc.name)
    await bot.add_cog(SetupMC(bot))
