"""The main roster file"""

from typing import Any, Dict
import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import get_guild_data_r, set_guild_data_r
from utils.validator import validate_interaction_guild, validate_permissions_r


class Roster(commands.Cog):
    """The main roster class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="create-roster", description="Create a roster")
    async def create_roster(
        self,
        interaction: discord.Interaction,
        roster_id: str,
        name: str,
        assign_role: discord.Role,
    ) -> None:
        """Handles the /croster command"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data_r(GUILD_ID)
        if roster_id in data["rosters"]:
            raise ValueError("Duplicate keys is not supported")
        data["rosters"][roster_id] = {
            "id": roster_id,
            "name": name,
            "members": {},
            "createdBy": str(interaction.user),
            "roleId": str(assign_role.id),
        }
        set_guild_data_r(GUILD_ID, data)
        await interaction.response.send_message(
            f"✅ Roster {name} created.", ephemeral=True
        )

    @app_commands.command(name="add-to-roster", description="Add a member to a roster")
    async def add_to_roster(
        self,
        interaction: discord.Interaction,
        roster_id: str,
        member: discord.Member,
        position: str,
    ) -> None:
        """Handles the /aroster command"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data_r(GUILD_ID)
        roster: Dict[str, Any] | None = data["rosters"].get(roster_id)
        if roster is None:
            await interaction.response.send_message(
                "❌ Roster not found.", ephemeral=True
            )
            return
        roster["members"][position] = str(member.id)
        data["rosters"][roster_id] = roster
        if roster["roleId"] is not None:
            role = guild.get_role(int(roster["roleId"]))
            if role is not None:
                await member.add_roles(
                    role, reason=f"{member.nick} got added to the roster {roster_id}!"
                )
            else:
                await interaction.response.send_message(
                    "Could not find role", ephemeral=True
                )
        set_guild_data_r(GUILD_ID, data)
        await interaction.response.send_message(
            f"✅ Added {member.mention} to roster {roster['name']} at {position}.",
            ephemeral=True,
        )

    @app_commands.command(name="remove-from-roster", description="Remove a member from a roster")
    async def remove_from_roster(
        self, interaction: discord.Interaction, roster_id: str, position: str
    ) -> None:
        """Handles the /rroster command"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data_r(GUILD_ID)
        roster: Dict[str, Any] | None = data["rosters"].get(roster_id)
        if roster is None or position not in roster["members"]:
            await interaction.response.send_message(
                "❌ Member not found.", ephemeral=True
            )
            return
        removed_id: int = int(roster["members"].pop(position))
        data["rosters"][roster_id] = roster
        member = guild.get_member(removed_id)
        if roster["roleId"] is not None and member is not None:
            role = guild.get_role(int(roster["roleId"]))
            if role is not None:
                await member.remove_roles(
                    role,
                    reason=f"{member.nick} got removed from the roster {roster_id}!",
                )
        set_guild_data_r(GUILD_ID, data)
        await interaction.response.send_message(
            f"🗑️ Removed <@{removed_id}> from roster {roster['name']} at {position}.",
            ephemeral=True,
        )

    @app_commands.command(name="delete-roster", description="Deletes the roster")
    async def delete_roster(self, interaction: discord.Interaction, roster_id: str):
        """Handles the /droster command"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data_r(GUILD_ID)
        try:
            del data["rosters"][roster_id]
            await interaction.response.send_message(
                f"🗑️✅ Roster {roster_id} has been deleted sucessfully!", ephemeral=True
            )
            set_guild_data_r(GUILD_ID, data)
            return
        except KeyError, ValueError:
            await interaction.response.send_message(
                f"Roster {roster_id} does not exist!", ephemeral=True
            )
            return


async def setup(bot: commands.Bot) -> None:
    """Prepares the bot"""
    await bot.add_cog(Roster(bot))
