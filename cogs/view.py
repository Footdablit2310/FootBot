"""Handles both the variants of the view command"""
from typing import Any, Dict
import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import get_guild_data
from utils.validator import validate_interaction_guild, validate_permissions


class PagedEmbed(discord.ui.View):
    """Handles Pages to not get stuck at embed limit"""
    def __init__(self, pages: list[discord.Embed]):
        super().__init__(timeout=None)
        self.pages = pages
        self.index = 0

        # Disable prev at start
        self.prev_button.disabled = True
        if len(pages) == 1:
            self.next_button.disabled = True

    @discord.ui.button(label="Prev", style=discord.ButtonStyle.secondary)
    async def prev_button(
        self, interaction: discord.Interaction, button: discord.ui.Button[Any]
    ):
        """This allows you to go to the prev page"""
        self.index -= 1
        if self.index <= 0:
            self.index = 0
            self.prev_button.disabled = True
        self.next_button.disabled = False
        await interaction.response.edit_message(embed=self.pages[self.index], view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next_button(
        self, interaction: discord.Interaction, button: discord.ui.Button[Any]
    ):
        """This allows you to go to the next page"""
        self.index += 1
        if self.index >= len(self.pages) - 1:
            self.index = len(self.pages) - 1
            self.next_button.disabled = True
        self.prev_button.disabled = False
        await interaction.response.edit_message(embed=self.pages[self.index], view=self)


class RosterSelect(discord.ui.Select[Any]):
    """Handles logic for /view-roster"""
    def __init__(self, rosters: Dict[str, Any], guild: discord.Guild):
        options = [
            discord.SelectOption(
                label="All", value="__all__", description="Show every roster"
            )
        ]
        options.extend(
            discord.SelectOption(label=r["name"], value=k) for k, r in rosters.items()
        )
        super().__init__(placeholder="Choose a roster...", options=options)
        self.rosters = rosters
        self.guild = guild

    async def callback(self, interaction: discord.Interaction):
        ephemeral = not validate_permissions(interaction)
        roster_id = self.values[0]
        if roster_id == "__all__":
            if not self.rosters:
                await interaction.response.send_message(
                    "No rosters found.", ephemeral=ephemeral
                )
                return

            embeds: list[discord.Embed] = []
            chunk: list[tuple[Any, str]] = []
            for i, (rid, roster) in enumerate(self.rosters.items(), start=1):
                role = self.guild.get_role(int(roster["roleId"]))
                role_text = role.mention if role else "❌ Invalid role assigned."
                member_count = len(roster.get("members", {}))
                chunk.append(
                    (
                        roster["name"],
                        f"ID: {rid}\n"
                        f"Created by <@{roster['createdBy']}>\n"
                        f"Role: {role_text}\n"
                        f"Members: {member_count}",
                    )
                )

                if i % 2 == 0 or i == len(self.rosters):
                    embed = discord.Embed(title="All rosters")
                    for name, value in chunk:
                        embed.add_field(name=name, value=value, inline=False)
                    embeds.append(embed)
                    chunk = []

            view = PagedEmbed(embeds)
            await interaction.response.send_message(
                embed=embeds[0], view=view, ephemeral=ephemeral
            )
            return

        roster: Dict[str, Any] = self.rosters[roster_id]
        embed = discord.Embed(
            title=f"Roster: {roster['name']}",
            description=f"Created by <@{roster['createdBy']}>",
        )
        embed.add_field(name="ID", value=roster_id, inline=True)
        role = self.guild.get_role(int(roster["roleId"]))
        if role is None:
            await interaction.response.send_message(
                "❌ Invalid role assigned.", ephemeral=ephemeral
            )
            return
        embed.add_field(
            name="Role", value=f"This roster has the assigned role {role.mention}"
        )
        for pos, uid in roster["members"].items():
            embed.add_field(name=pos, value=f"<@{uid}>", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


class EventSelect(discord.ui.Select[Any]):
    """Handles logic for /view-event"""
    def __init__(self, events: Dict[str, Any]):
        options = [
            discord.SelectOption(
                label="All", value="__all__", description="Show every event"
            )
        ]
        options.extend(
            discord.SelectOption(label=e["title"], value=k) for k, e in events.items()
        )
        super().__init__(placeholder="Choose an event...", options=options)
        self.events = events

    async def callback(self, interaction: discord.Interaction):
        ephemeral = not validate_permissions(interaction)
        event_id = self.values[0]
        if event_id == "__all__":
            if not self.events:
                await interaction.response.send_message(
                    "No events found.", ephemeral=ephemeral
                )
                return

            embeds: list[discord.Embed] = []
            chunk: list[tuple[Any, str]] = []
            for i, (eid, event) in enumerate(self.events.items(), start=1):
                value = (
                    f"ID: {eid}\n"
                    f"Created by <@{event['createdBy']}>\n"
                    f"Time: <t:{event['dateUnix']}:F>"
                )
                if event.get("rosterId"):
                    value += f"\nRoster: {event['rosterId']}"
                if event.get("linkedDiscordEventId"):
                    value += f"\nLinked Discord Event: {event['linkedDiscordEventId']}"
                chunk.append((event["title"], value))

                if i % 2 == 0 or i == len(self.events):
                    embed = discord.Embed(title="All events")
                    for name, val in chunk:
                        embed.add_field(name=name, value=val, inline=False)
                    embeds.append(embed)
                    chunk = []

            view = PagedEmbed(embeds)
            await interaction.response.send_message(
                embed=embeds[0], view=view, ephemeral=ephemeral
            )
            return

        event: Dict[str, Any] = self.events[event_id]
        embed = discord.Embed(
            title=f"Event: {event['title']}",
            description=f"Created by <@{event['createdBy']}>",
        )
        embed.add_field(name="ID", value=event_id, inline=True)
        embed.add_field(name="Time", value=f"<t:{event['dateUnix']}:F>", inline=True)
        if event.get("rosterId"):
            embed.add_field(name="Roster", value=event["rosterId"], inline=True)
        if event.get("linkedDiscordEventId"):
            embed.add_field(
                name="Linked Discord Event",
                value=event["linkedDiscordEventId"],
                inline=True,
            )
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


class View(commands.Cog):
    """The view base class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="view-roster", description="View roster details")
    async def view_roster(self, interaction: discord.Interaction):
        """The actual command"""
        ephemeral = not validate_permissions(interaction)
        guild = validate_interaction_guild(interaction)
        data = get_guild_data(guild.id)
        rosters = data["rosters"]
        view = discord.ui.View()
        view.add_item(RosterSelect(rosters, guild))
        await interaction.response.send_message(
            "Select a roster:", view=view, ephemeral=ephemeral
        )

    @app_commands.command(name="view-event", description="View event details")
    async def view_event(self, interaction: discord.Interaction):
        """The actual command"""
        ephemeral = not validate_permissions(interaction)
        guild = validate_interaction_guild(interaction)
        data = get_guild_data(guild.id)
        events = data["events"]
        view = discord.ui.View()
        view.add_item(EventSelect(events))
        await interaction.response.send_message(
            "Select an event:", view=view, ephemeral=ephemeral
        )


async def setup(bot: commands.Bot) -> None:
    """This handles setup"""
    await bot.add_cog(View(bot))
