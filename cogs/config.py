"""Config handling file"""

from typing import Optional, Any, Dict
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from utils.storage import get_guild_data, set_guild_data
from utils.validator import validate_interaction_guild, validate_permissions


class Config(commands.Cog):
    """The config class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="permissions", description="View and Edit Role and Member Permissions"
    )
    async def permissions(
        self,
        interaction: discord.Interaction,
        values: Optional[list[discord.Role | discord.Member]],
    ):
        """
        Handles ALL Permissions for a Guild
        """
        if not validate_permissions(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Dict[str, Any]] = get_guild_data(GUILD_ID)
        permissions_config: dict[str, list[int]] = data["config"]["permissions"]
        str_lst: list[str] = []
        permissions_config["roles"] = []
        permissions_config["members"] = []
        if values is not None:
            for value in values:
                if isinstance(value, discord.Role):
                    permissions_config["roles"].append(value.id)
                    set_guild_data(GUILD_ID, data)
                else:
                    permissions_config["members"].append(value.id)
                    set_guild_data(GUILD_ID, data)
            for k, v in permissions_config.items():
                str_lst.append(f"{k} : {v}")
            await interaction.response.send_message(
                f"⚙️ New permissions: {"\n".join(str_lst)}", ephemeral=True
            )
        else:
            for k, v in permissions_config.items():
                str_lst.append(f"{k} : {v}")
            await interaction.response.send_message(
                f"⚙️ Current permissions: {"\n".join(str_lst)}", ephemeral=True
            )

    @app_commands.command(name="config", description="View or update bot config")
    @app_commands.commands.choices(
        key=[
            Choice(name="pingMinutesBefore", value="pingMinutesBefore"),
            Choice(name="eventChannelId", value="eventChannelId"),
        ]
    )
    async def config(
        self,
        interaction: discord.Interaction,
        key: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        """The async Config method"""
        if not validate_permissions(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Dict[str, Any]] = get_guild_data(GUILD_ID)
        if key and value:
            data["config"][key] = value
            set_guild_data(GUILD_ID, data)
            await interaction.response.send_message(
                f"⚙️ Config {key} updated to {value}.", ephemeral=True
            )
            return
        str_lst: list[str] = []
        for k, v in data["config"].items():
            if k != "permissions":
                str_lst.append(f"{k} : {v}")
        await interaction.response.send_message(
            f"⚙️ Current config: {"\n".join(str_lst)}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    """Prepares Bot"""
    await bot.add_cog(Config(bot))
