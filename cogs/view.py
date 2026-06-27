import discord
from discord.ext import commands
from discord import app_commands
from typing import Any, Dict
from utils.storage import get_guild_data
from utils.validator import validate_interaction_guild

class View(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="view", description="View roster or event details")
    async def view(self, interaction: discord.Interaction, kind: str, id: str) -> None:
        guild=validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data(GUILD_ID)

        if kind == "roster":
            roster: Dict[str, Any] | None = data["rosters"].get(id)
            if roster is None:
                await interaction.response.send_message("❌ Roster not found.")
                return
            embed: discord.Embed = discord.Embed(
                title=f"Roster: {roster['name']}",
                description=f"Created by <@{roster['createdBy']}>"
            )
            for pos, uid in roster["members"].items():
                embed.add_field(name=pos, value=f"<@{uid}>", inline=True)
            await interaction.response.send_message(embed=embed)

        elif kind == "event":
            ev: Dict[str, Any] | None = data["events"].get(id)
            if ev is None:
                await interaction.response.send_message("❌ Event not found.")
                return
            embed: discord.Embed = discord.Embed(
                title=f"Event: {ev['title']}",
                description=f"Created by <@{ev['createdBy']}>"
            )
            embed.add_field(name="ID", value=ev["id"], inline=True)
            embed.add_field(name="Time", value=f"<t:{ev['dateUnix']}:F>", inline=True)
            if ev.get("rosterId"):
                embed.add_field(name="Roster", value=ev["rosterId"], inline=True)
            await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message("❌ Invalid kind. Use 'roster' or 'event'.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(View(bot))
