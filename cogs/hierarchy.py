"""Hierarchy"""

from typing import Any, Dict, List
import discord
from discord import app_commands
from discord.ext import commands
from utils.validator import validate_interaction_guild, validate_permissions_l
from utils.storage import get_guild_data_l, set_guild_data_l


class Hierarchy(commands.Cog):
    """Cog providing custom hierarchy commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(
        name="add-rank", description="Add a role to the custom hierarchy"
    )
    @app_commands.describe(
        role="Role to add", position="Position in hierarchy (1 = top)"
    )
    async def add_rank(
        self, interaction: discord.Interaction, role: discord.Role, position: int
    ) -> None:
        """Adds a rank to hierarchy"""
        if not validate_permissions_l(interaction):
            await interaction.response.send_message(
                "You do not have access", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        hierarchy: List[int] = guild_data.get("hierarchy", [])

        # Insert role at desired position (adjust for 0-based index)
        if position < 1:
            position = 1
        if position > len(hierarchy) + 1:
            position = len(hierarchy) + 1

        hierarchy.insert(position - 1, role.id)
        guild_data["hierarchy"] = hierarchy
        set_guild_data_l(guild.id, guild_data)

        await interaction.response.send_message(
            f"Added {role.mention} at position {position} in the hierarchy.",
            ephemeral=True,
        )

    @app_commands.command(
        name="view-hierarchy", description="View the custom role hierarchy"
    )
    async def view_hierarchy(self, interaction: discord.Interaction) -> None:
        """View hierarchy"""
        guild = validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        hierarchy: List[int] = guild_data.get("hierarchy", [])

        if not hierarchy:
            await interaction.response.send_message(
                "No custom hierarchy set.", ephemeral=True
            )
            return

        roles = [guild.get_role(rid) for rid in hierarchy if guild.get_role(rid)]
        embed = discord.Embed(
            title=f"Custom Hierarchy for {guild.name}",
            description="\n".join(f"{i+1}. {r.mention}" for i, r in enumerate(roles)),  # type: ignore
            color=discord.Color.gold(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="reset-hierarchy", description="Clear the custom hierarchy"
    )
    async def reset_hierarchy(self, interaction: discord.Interaction) -> None:
        """Resets the hierarchy"""
        if not validate_permissions_l(interaction):
            await interaction.response.send_message(
                "You do not have access", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        guild_data["hierarchy"] = []
        set_guild_data_l(guild.id, guild_data)

        await interaction.response.send_message(
            "Hierarchy has been reset.", ephemeral=True
        )

async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot by adding the Hierarchy Cog."""
    await bot.add_cog(Hierarchy(bot))