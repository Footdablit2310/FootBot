"""The Map Cog"""
from typing import Any, Dict, List
import discord
from discord import app_commands
from discord.ext import commands
from utils.validator import validate_interaction_guild
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
        map_file="Upload the map file"
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
        route: str | None = None
    ) -> None:
        """Handles the /create-map command."""
        difficulty_value: str = difficulty if difficulty else role.name
        route_value: str = route if route else "None"
        guild: discord.Guild = validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        maps_data: List[Dict[str, Any]] = guild_data.get("maps", [])
        maps_data.append({
            "name": name,
            "difficulty": difficulty_value,
            "points": points,
            "credit": credit.id,
            "role_required": role.id,
            "map_file": {
                "filename": map_file.filename,
                "url": map_file.url,
                "id": map_file.id
            },
            "route": route_value
        })
        guild_data["maps"] = maps_data
        set_guild_data_l(guild.id, guild_data)

        await interaction.response.send_message(f"Map **{name}** created and stored.", ephemeral=True)

    @app_commands.command(name="view-map", description="View details of a stored map")
    async def view_map(self, interaction: discord.Interaction) -> None:
        """
        Handles the /view-map command.
        Shows a select menu of all maps stored for the guild.
        """
        guild: discord.Guild = validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        maps_data: List[Dict[str, Any]] = guild_data.get("maps", [])

        if not maps_data:
            await interaction.response.send_message("No maps available.", ephemeral=True)
            return

        options: List[discord.SelectOption] = [
            discord.SelectOption(label=m["name"], description=f"{m['difficulty']} ({m['points']} pts)")
            for m in maps_data
        ]

        view: MapSelectView = MapSelectView(maps_data, guild)
        view.add_item(discord.ui.Select(placeholder="Choose a map", options=options, custom_id="map_select"))

        await interaction.response.send_message("Select a map to view:", view=view, ephemeral=True)


class MapSelectView(discord.ui.View):
    """Interactive view for selecting and displaying a map."""

    def __init__(self, maps_data: List[Dict[str, Any]], guild: discord.Guild) -> None:
        """Initialize the map selection view."""
        super().__init__(timeout=60)
        self.maps_data: List[Dict[str, Any]] = maps_data
        self.guild: discord.Guild = guild

    @discord.ui.select(custom_id="map_select")
    async def map_select(self, interaction: discord.Interaction, select: discord.ui.Select[Any]) -> None:
        """Handle map selection and display its details."""
        mapname: str = select.values[0]
        chosen_map: Dict[str, Any] = next(m for m in self.maps_data if m["name"] == mapname)

        credit_member: discord.Member | None = self.guild.get_member(chosen_map["credit"])
        role_required: discord.Role | None = self.guild.get_role(chosen_map["role_required"])

        embed: discord.Embed = discord.Embed(
            title=chosen_map["name"],
            color=discord.Color.green()
        )
        embed.add_field(name="Difficulty", value=chosen_map["difficulty"], inline=True)
        embed.add_field(name="Points", value=str(chosen_map["points"]), inline=True)
        embed.add_field(name="Credit", value=credit_member.mention if credit_member else f"User {chosen_map['credit']}", inline=True)
        embed.add_field(name="Role Required", value=role_required.mention if role_required else f"Role {chosen_map['role_required']}", inline=True)
        embed.add_field(name="Map File", value=f"[{chosen_map['map_file']['filename']}]({chosen_map['map_file']['url']})", inline=False)
        embed.add_field(name="Route", value=chosen_map["route"], inline=False)

        await interaction.response.edit_message(content=None, embed=embed, view=None)


async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot by adding the Map Cog."""
    await bot.add_cog(Map(bot))
