"""Config handling file"""

from typing import Optional, Any, Dict
import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import get_guild_data, set_guild_data
from utils.validator import validate_interaction_guild


class Config(commands.Cog):
    """The config class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="config", description="View or update bot config")
    async def config(
        self,
        interaction: discord.Interaction,
        key: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        """The async Config method"""
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data(GUILD_ID)
        if key and value:
            data["config"][key] = value
            set_guild_data(GUILD_ID, data)
            await interaction.response.send_message(
                f"⚙️ Config {key} updated to {value}.", ephemeral=True
            )
            return
        await interaction.response.send_message(
            f"⚙️ Current config: {data['config']}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    """Prepares Bot"""
    await bot.add_cog(Config(bot))
