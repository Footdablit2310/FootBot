"""Config handling file"""

from typing import Optional, Any, Dict
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from utils.storage import (
    get_guild_data_r,
    set_guild_data_r,
    get_guild_data_l,
    set_guild_data_l,
)
from utils.validator import validate_interaction_guild, validate_permissions_r


class Config(commands.Cog):
    """The config class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="apermissions-roster", description="Add a role or member to permissions"
    )
    async def apermissions_roster(
        self,
        interaction: discord.Interaction,
        role: Optional[discord.Role] = None,
        member: Optional[discord.Member] = None,
    ):
        """Adds permissions"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return

        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data = get_guild_data_r(GUILD_ID)
        permissions_config: dict[str, list[int]] = data["config"]["permissions"]

        if role:
            permissions_config["roles"].append(role.id)
        if member:
            permissions_config["members"].append(member.id)

        set_guild_data_r(GUILD_ID, data)
        role_mentions: list[str] = []
        for rid in permissions_config["roles"]:
            role = guild.get_role(rid)
            if role is not None:
                role_mentions.append(role.mention)
            else:
                role_mentions.append(f"❌ Invalid role {rid}")

        member_mentions: list[str] = []
        for mid in permissions_config["members"]:
            member = guild.get_member(mid)
            if member is not None:
                member_mentions.append(member.mention)
            else:
                member_mentions.append(f"❌ Invalid member {mid}")

        # Build response with mentions
        if role or member:
            msg = "⚙️ Added permissions:\n"
        else:
            msg = "⚙️ Current permissions:\n"

        msg = (
            f"Roles: {', '.join(role_mentions) if role_mentions else 'None'}\n"
            f"Members: {', '.join(member_mentions) if member_mentions else 'None'}"
        )

        await interaction.response.send_message(msg, ephemeral=True)

    @app_commands.command(
        name="rpermissions-roster",
        description="Remove a role or member from permissions",
    )
    async def rpermissions_roster(
        self,
        interaction: discord.Interaction,
        role: Optional[discord.Role] = None,
        member: Optional[discord.Member] = None,
    ):
        """Removes permissions"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return

        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data = get_guild_data_r(GUILD_ID)
        permissions_config: dict[str, list[int]] = data["config"]["permissions"]

        if role and role.id in permissions_config["roles"]:
            permissions_config["roles"].remove(role.id)
        if member and member.id in permissions_config["members"]:
            permissions_config["members"].remove(member.id)

        set_guild_data_r(GUILD_ID, data)
        role_mentions: list[str] = []
        for rid in permissions_config["roles"]:
            role = guild.get_role(rid)
            if role is not None:
                role_mentions.append(role.mention)
            else:
                role_mentions.append(f"❌ Invalid role {rid}")

        member_mentions: list[str] = []
        for mid in permissions_config["members"]:
            member = guild.get_member(mid)
            if member is not None:
                member_mentions.append(member.mention)
            else:
                member_mentions.append(f"❌ Invalid member {mid}")

        if role or member:
            msg = "⚙️ Removed permissions:\n"
        else:
            msg = "⚙️ Current permissions:\n"

        msg = (
            f"Roles: {', '.join(role_mentions) if role_mentions else 'None'}\n"
            f"Members: {', '.join(member_mentions) if member_mentions else 'None'}"
        )

        await interaction.response.send_message(msg, ephemeral=True)

    @app_commands.command(
        name="apermissions-leaderboard",
        description="Add a role or member to permissions",
    )
    async def apermissions_leaderboard(
        self,
        interaction: discord.Interaction,
        role: Optional[discord.Role] = None,
        member: Optional[discord.Member] = None,
    ):
        """Adds permissions"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return

        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data = get_guild_data_l(GUILD_ID)
        permissions_config: dict[str, list[int]] = data["config"]["permissions"]

        if role:
            permissions_config["roles"].append(role.id)
        if member:
            permissions_config["members"].append(member.id)

        set_guild_data_l(GUILD_ID, data)
        role_mentions: list[str] = []
        for rid in permissions_config["roles"]:
            role = guild.get_role(rid)
            if role is not None:
                role_mentions.append(role.mention)
            else:
                role_mentions.append(f"❌ Invalid role {rid}")

        member_mentions: list[str] = []
        for mid in permissions_config["members"]:
            member = guild.get_member(mid)
            if member is not None:
                member_mentions.append(member.mention)
            else:
                member_mentions.append(f"❌ Invalid member {mid}")

        # Build response with mentions
        if role or member:
            msg = "⚙️ Added permissions:\n"
        else:
            msg = "⚙️ Current permissions:\n"

        msg = (
            f"Roles: {', '.join(role_mentions) if role_mentions else 'None'}\n"
            f"Members: {', '.join(member_mentions) if member_mentions else 'None'}"
        )

        await interaction.response.send_message(msg, ephemeral=True)

    @app_commands.command(
        name="rpermissions-leaderboard",
        description="Remove a role or member from permissions",
    )
    async def rpermissions_leaderboard(
        self,
        interaction: discord.Interaction,
        role: Optional[discord.Role] = None,
        member: Optional[discord.Member] = None,
    ):
        """Removes permissions"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return

        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data = get_guild_data_l(GUILD_ID)
        permissions_config: dict[str, list[int]] = data["config"]["permissions"]

        if role and role.id in permissions_config["roles"]:
            permissions_config["roles"].remove(role.id)
        if member and member.id in permissions_config["members"]:
            permissions_config["members"].remove(member.id)

        set_guild_data_l(GUILD_ID, data)
        role_mentions: list[str] = []
        for rid in permissions_config["roles"]:
            role = guild.get_role(rid)
            if role is not None:
                role_mentions.append(role.mention)
            else:
                role_mentions.append(f"❌ Invalid role {rid}")

        member_mentions: list[str] = []
        for mid in permissions_config["members"]:
            member = guild.get_member(mid)
            if member is not None:
                member_mentions.append(member.mention)
            else:
                member_mentions.append(f"❌ Invalid member {mid}")

        if role or member:
            msg = "⚙️ Removed permissions:\n"
        else:
            msg = "⚙️ Current permissions:\n"

        msg = (
            f"Roles: {', '.join(role_mentions) if role_mentions else 'None'}\n"
            f"Members: {', '.join(member_mentions) if member_mentions else 'None'}"
        )

        await interaction.response.send_message(msg, ephemeral=True)

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
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Dict[str, Any]] = get_guild_data_r(GUILD_ID)
        if key and value:
            data["config"][key] = value
            set_guild_data_r(GUILD_ID, data)
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
