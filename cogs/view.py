
from typing import Any, Dict
import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import get_guild_data
from utils.validator import validate_interaction_guild


class RosterSelect(discord.ui.Select[Any]):
    def __init__(self, rosters: Dict[str, Any], guild: discord.Guild):
        options = [discord.SelectOption(label=r) for r in rosters.keys()]
        super().__init__(placeholder="Choose a roster...", options=options)
        self.rosters = rosters
        self.guild = guild

    async def callback(self, interaction: discord.Interaction):
        roster_id = self.values[0]
        roster: Dict[str, Any] = self.rosters[roster_id]
        embed = discord.Embed(
            title=f"Roster: {roster['name']}",
            description=f"Created by <@{roster['createdBy']}>",
        )
        role = self.guild.get_role(int(roster["roleId"]))
        if role is None:
            await interaction.response.send_message(
                "❌ Invalid role assigned.", ephemeral=True
            )
            return
        embed.add_field(
            name="Role", value=f"This roster has the assigned role {role.mention}"
        )
        for pos, uid in roster["members"].items():
            embed.add_field(name=pos, value=f"<@{uid}>", inline=True)
        await interaction.response.send_message(embed=embed)


class EventSelect(discord.ui.Select[Any]):
    def __init__(self, events: Dict[str, Any]):
        options = [discord.SelectOption(label=e) for e in events.keys()]
        super().__init__(placeholder="Choose an event...", options=options)
        self.events = events

    async def callback(self, interaction: discord.Interaction):
        event_id = self.values[0]
        event: Dict[str, Any] = self.events[event_id]
        embed = discord.Embed(
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


class View(commands.Cog):
    """The view base class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="view-roster", description="View roster details")
    async def view_roster(self, interaction: discord.Interaction):
        guild = validate_interaction_guild(interaction)
        data = get_guild_data(guild.id)
        rosters = data["rosters"]
        view = discord.ui.View()
        view.add_item(RosterSelect(rosters, guild))
        await interaction.response.send_message(
            "Select a roster:", view=view, ephemeral=True
        )

    @app_commands.command(name="view-event", description="View event details")
    async def view_event(self, interaction: discord.Interaction):
        guild = validate_interaction_guild(interaction)
        data = get_guild_data(guild.id)
        events = data["events"]
        view = discord.ui.View()
        view.add_item(EventSelect(events))
        await interaction.response.send_message(
            "Select an event:", view=view, ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(View(bot))
