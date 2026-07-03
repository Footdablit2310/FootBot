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
    @app_commands.describe(
        name="Name of the map to view"
    )
    async def view_map(
        self,
        interaction: discord.Interaction,
        name: str
    ) -> None:
        """
        Handles the /view-map command.
        Looks up a map by name in guild storage and displays its details.
        """
        guild: discord.Guild = validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        maps_data: List[Dict[str, Any]] = guild_data.get("maps", [])

        chosen_map: Dict[str, Any] | None = next((m for m in maps_data if m["name"].lower() == name.lower()), None)
        if not chosen_map:
            await interaction.response.send_message(f"No map named **{name}** found.", ephemeral=True)
            return

        credit_member: discord.Member | None = guild.get_member(chosen_map["credit"])
        role_required: discord.Role | None = guild.get_role(chosen_map["role_required"])

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

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot by adding the Map Cog."""
    await bot.add_cog(Map(bot))
