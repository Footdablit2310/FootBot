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
        roles: Optional[list[discord.Role]] = None,
        members: Optional[list[discord.Member]] = None,
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
        data: dict[str, Any] = get_guild_data(GUILD_ID)["config"]["permissions"]
        permissions_config: dict[str, list[int]] = data

        # Reset permissions
        permissions_config["roles"] = []
        permissions_config["members"] = []

        # Update roles
        if roles is not None:
            for role in roles:
                permissions_config["roles"].append(role.id)

        # Update members
        if members is not None:
            for member in members:
                permissions_config["members"].append(member.id)

        # Save changes
        set_guild_data(GUILD_ID, data)

        # Build response string
        str_lst = [f"{k}: {v}" for k, v in permissions_config.items()]

        if roles or members:
            await interaction.response.send_message(
                "⚙️ New permissions:\n" + "\n".join(str_lst), ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "⚙️ Current permissions:\n" + "\n".join(str_lst), ephemeral=True
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
