"""The file with Map Cog"""
from typing import Any
import discord
from discord import app_commands
from discord.ext import commands
from utils.validator import validate_interaction_guild
from utils.storage import get_guild_data_l, set_guild_data_l

class Map(commands.Cog):
    """The Map Cog"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

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
    ):
        """Handles the /create-map command"""
        difficulty_value = difficulty if difficulty else role.name
        route_value = route if route else "None"
        guild=validate_interaction_guild(interaction)
        guild_data = get_guild_data_l(guild.id)
        maps_data:list[dict[str, Any]] = guild_data.get("maps", [])
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

async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot"""
    await bot.add_cog(Map(bot))