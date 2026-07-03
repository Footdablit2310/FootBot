"""The Map Cog"""

from typing import Any, Dict, List
import discord
from discord import app_commands
from discord.ext import commands
from utils.validator import (
    validate_interaction_guild,
    validate_permissions_l,
    can_access_role,
)
from utils.storage import get_guild_data_l, set_guild_data_l


class Map(commands.Cog):
    """Cog providing map management commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the Map Cog."""
        self.bot: commands.Bot = bot

    @app_commands.command(name="create-map", description="Create a new map entry")
    @app_commands.describe(
        name="Map name",
        difficulty="Difficulty (optional)",
        points="Award points",
        credit="Member credited",
        route="Route URL (optional)",
        role="Role required",
        map_file="Upload the map file",
    )
    async def create_map(
        self,
        interaction: discord.Interaction,
        name: str,
        points: int,
        credit: discord.Member,
        role: discord.Role,
        map_file: discord.Attachment,
        difficulty: str | None = None,
        route: str | None = None,
    ) -> None:
        """Handles the /create-map command."""
        if not validate_permissions_l(interaction):
            await interaction.response.send_message(
                "You do not have access", ephemeral=True
            )
            return
        difficulty_value: str = difficulty if difficulty else role.name
        route_value: str = route if route else "None"
        guild: discord.Guild = validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        maps_data: List[Dict[str, Any]] = guild_data.get("maps", [])
        maps_data.append(
            {
                "name": name,
                "difficulty": difficulty_value,
                "points": points,
                "credit": credit.id,
                "role_required": role.id,
                "map_file": {
                    "filename": map_file.filename,
                    "url": map_file.url,
                    "id": map_file.id,
                },
                "route": route_value,
            }
        )
        guild_data["maps"] = maps_data
        set_guild_data_l(guild.id, guild_data)

        await interaction.response.send_message(
            f"Map **{name}** created and stored.", ephemeral=True
        )
    @app_commands.command(name="delete-map", description="Delete a stored map")
    @app_commands.describe(name="Name of the map to delete")
    async def delete_map(self, interaction: discord.Interaction, name: str) -> None:
        """
        Handles the /delete-map command.
        Deletes a map entry if the user has permission (role at or below their rank).
        """
        if not validate_permissions_l(interaction):
            await interaction.response.send_message("You do not have access to this command!")
            return
        guild: discord.Guild = validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        maps_data: List[Dict[str, Any]] = guild_data.get("maps", [])

        # Find the map by name
        chosen_map = next((m for m in maps_data if m["name"].lower() == name.lower()), None)
        if not chosen_map:
            await interaction.response.send_message(
                f"No map named **{name}** found.", ephemeral=True
            )
            return

        # Remove the map
        maps_data.remove(chosen_map)
        guild_data["maps"] = maps_data
        set_guild_data_l(guild.id, guild_data)

        await interaction.response.send_message(
            f"Map **{name}** has been deleted.", ephemeral=True
        )

    @app_commands.command(name="view-map", description="View maps for a specific role")
    @app_commands.describe(role="Role whose maps you want to view")
    async def view_map(
        self, interaction: discord.Interaction, role: discord.Role
    ) -> None:
        """
        Handles the /view-map command.
        Shows a select menu of maps stored for the guild, filtered by role.
        """
        if not can_access_role(interaction, role):
            await interaction.response.send_message(
                "You cannot view maps higher than your rank!", ephemeral=True
            )
            return
        guild: discord.Guild = validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        maps_data: List[Dict[str, Any]] = guild_data.get("maps", [])
        # Filter maps by the given role
        role_maps = [m for m in maps_data if m["role_required"] == role.id]

        if not role_maps:
            await interaction.response.send_message(
                f"No maps available for role {role.mention}.", ephemeral=True
            )
            return

        view = MapSelectView(role_maps, guild)
        await interaction.response.send_message(
            f"Select a map for {role.mention}:", view=view, ephemeral=True
        )


class MapSelectView(discord.ui.View):
    """Interactive view for selecting and displaying a map."""

    def __init__(self, maps_data: list[dict[str, Any]], guild: discord.Guild) -> None:
        super().__init__(timeout=60)
        self.maps_data = maps_data
        self.guild = guild

        options = [
            discord.SelectOption(
                label=m["name"],
                description=f"{m['difficulty']} ({m['points']} pts)",
                value=str(i),  # use index as stable value
            )
            for i, m in enumerate(maps_data)
        ]

        select: discord.ui.Select[Any] = discord.ui.Select(
            placeholder="Choose a map", options=options, min_values=1, max_values=1
        )

        async def on_select(interaction: discord.Interaction):
            index = int(interaction.data["values"][0])  # type: ignore
            chosen_map = self.maps_data[index]

            credit_member = self.guild.get_member(chosen_map["credit"])
            role_required = self.guild.get_role(chosen_map["role_required"])

            embed = discord.Embed(title=chosen_map["name"], color=discord.Color.green())
            embed.add_field(
                name="Difficulty", value=chosen_map["difficulty"], inline=True
            )
            embed.add_field(name="Points", value=str(chosen_map["points"]), inline=True)
            embed.add_field(
                name="Credit",
                value=(
                    credit_member.mention
                    if credit_member
                    else f"User {chosen_map['credit']}"
                ),
                inline=True,
            )
            embed.add_field(
                name="Role Required",
                value=(
                    role_required.mention
                    if role_required
                    else f"Role {chosen_map['role_required']}"
                ),
                inline=True,
            )
            embed.add_field(
                name="Map File",
                value=f"[{chosen_map['map_file']['filename']}]({chosen_map['map_file']['url']})",
                inline=False,
            )
            embed.add_field(name="Route", value=chosen_map["route"], inline=False)

            await interaction.response.edit_message(
                content=None, embed=embed, view=None
            )

        select.callback = on_select
        self.add_item(select)


async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot by adding the Map Cog."""
    await bot.add_cog(Map(bot))
