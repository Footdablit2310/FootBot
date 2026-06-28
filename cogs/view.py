"""The file handling all te view commands"""

from typing import Any, Dict, List
import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import get_guild_data
from utils.validator import validate_interaction_guild


class View(commands.Cog):
    """THe view base class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(
        name="view-roster", description="View roster details"
    )
    async def view_roster(self, interaction: discord.Interaction) -> None:
        """Handles the /view roster command"""
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data(GUILD_ID)
        rosters: Dict[str, Any] = data["rosters"]
        MenuOptions: List[discord.SelectOption] = []
        for r in list(rosters.keys()):
            MenuOptions.append(discord.SelectOption(label=r))
        roster_id: str = discord.ui.Select(options=MenuOptions).values[0]
        roster: Dict[str, Any] = rosters[roster_id]
        embed: discord.Embed = discord.Embed(
            title=f"Roster: {roster['name']}",
            description=f"Created by <@{roster['createdBy']}>",
        )
        role=guild.get_role(roster["roleId"])
        if role is None:
            raise ValueError("Impossible Role Value")
        embed.add_field(name="Role", value=f"This roster has the assigned role {role.mention}")
        for pos, uid in roster["members"].items():
            embed.add_field(name=pos, value=f"<@{uid}>", inline=True)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="view-event", description="View event details.")
    async def view_event(
        self,
        interaction: discord.Interaction,
    ):
        """Handles the /view event command"""
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data(GUILD_ID)
        events: Dict[str, Any] = data["events"]
        MenuOptions: List[discord.SelectOption] = []
        for r in list(events.keys()):
            MenuOptions.append(discord.SelectOption(label=r))
        event_id: str = discord.ui.Select(options=MenuOptions).values[0]
        event: Dict[str, Any] = events[event_id]
        embed: discord.Embed = discord.Embed(
            title=f"Event: {event['title']}",
            description=f"Created by <@{event['createdBy']}>",
        )
        embed.add_field(name="ID", value=event["id"], inline=True)
        embed.add_field(name="Time", value=f"<t:{event['dateUnix']}:F>", inline=True)
        if event.get("rosterId"):
            embed.add_field(name="Roster", value=event["rosterId"], inline=True)
        if event.get("linkedDiscordEventId"):
            embed.add_field(
                name="Linked Discord Event",
                value=event["linkedDiscordEventId"],
                inline=True,
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot"""
    await bot.add_cog(View(bot))
