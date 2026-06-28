"""Handles events"""

import datetime
from typing import Any, Dict, Optional
import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import get_guild_data, set_guild_data
from utils.validator import validate_interaction_guild
from utils.timecalender import CalendarView
from bot import log

class Events(commands.Cog):
    """The event base class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="cevent", description="Create an event")
    async def cevent(
        self,
        interaction: discord.Interaction,
        event_id: str,
        title: str,
        roster_id: Optional[str] = None,
    ) -> None:
        """Create Event"""
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data(GUILD_ID)

        def finalize(unix_ts: int) -> None:
            data["events"][event_id] = {
                "id": event_id,
                "title": title,
                "dateUnix": unix_ts,
                "rosterId": roster_id,
                "createdBy": str(interaction.user.id),
                "pinged": False,
                "linkedDiscordEventId": None,
            }
            set_guild_data(GUILD_ID, data)
            log.info("Event saved!")

        now: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        view: CalendarView = CalendarView(now.year, now.month, finalize)

        embed = discord.Embed(title="📅 Pick a Date", description="Use the buttons below to select.", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


    @app_commands.command(name="devent", description="Delete an event")
    async def devent(self, interaction: discord.Interaction, event_id: str) -> None:
        """Handles the /devent command"""
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data(GUILD_ID)
        if event_id in data["events"]:
            del data["events"][event_id]
            set_guild_data(GUILD_ID, data)
            await interaction.response.send_message(
                f"🗑️ Event {event_id} deleted.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Event not found.", ephemeral=True
            )

    @app_commands.command(name="eevent", description="Edit an event")
    async def eevent(
        self,
        interaction: discord.Interaction,
        event_id: str,
        new_title: Optional[str] = None,
        new_unix_time: Optional[int] = None,
    ) -> None:
        """Handles the /eevent command"""
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data(GUILD_ID)
        ev: Dict[str, Any] | None = data["events"].get(event_id)
        if ev is None:
            await interaction.response.send_message(
                "❌ Event not found.", ephemeral=True
            )
            return
        if new_title is not None:
            ev["title"] = new_title
        if new_unix_time is not None:
            ev["dateUnix"] = new_unix_time
        data["events"][event_id] = ev
        set_guild_data(GUILD_ID, data)
        await interaction.response.send_message(
            f"✏️ Event {event_id} updated.", ephemeral=True
        )

    @app_commands.command(
        name="levent", description="Link a FootBot event to a Discord Scheduled Event"
    )
    async def levent(
        self, interaction: discord.Interaction, event_id: str, discord_event_id: int
    ) -> None:
        """Link a FootBot event to a Discord Scheduled Event by ID."""
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data(GUILD_ID)
        ev: Dict[str, Any] | None = data["events"].get(event_id)
        if ev is None:
            await interaction.response.send_message(
                "❌ Event not found.", ephemeral=True
            )
            return

        # Fetch the scheduled event object manually
        scheduled_event: Optional[discord.ScheduledEvent] = guild.get_scheduled_event(
            discord_event_id
        )
        if scheduled_event is None:
            await interaction.response.send_message(
                "❌ Discord Scheduled Event not found.", ephemeral=True
            )
            return

        ev["linkedDiscordEventId"] = str(scheduled_event.id)
        data["events"][event_id] = ev
        set_guild_data(GUILD_ID, data)

        await interaction.response.send_message(
            f"🔗 Linked FootBot event {event_id} to Discord event {scheduled_event.name}.",
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot"""
    await bot.add_cog(Events(bot))
