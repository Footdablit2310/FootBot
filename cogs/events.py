"""Handles events"""

import datetime
from typing import Any, Dict, Optional
import pytz
import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import get_guild_data_r, set_guild_data_r, command_list_add
from utils.validator import validate_interaction_guild, validate_permissions_r


class Events(commands.Cog):
    """The event base class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="create-event", description="Create an event")
    @app_commands.commands.describe(
        time="Time in 24h format in this format: YYYY/MM/DD-HH:MM"
    )
    async def create_event(
        self,
        interaction: discord.Interaction,
        event_id: str,
        title: str,
        time: str,
        tz_name: Optional[str],
        roster_id: Optional[str] = None,
    ) -> None:
        """Create Event"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        # Parse the string into a datetime
        try:
            dt_naive = datetime.datetime.strptime(time, "%Y/%m/%d-%H:%M")
            tz = pytz.timezone(tz_name if tz_name is not None else "UTC")
            dt_local = tz.localize(dt_naive)
            dt_utc = dt_local.astimezone(datetime.timezone.utc)
            unix_ts = int(dt_utc.timestamp())
            data: Dict[str, Any] = get_guild_data_r(GUILD_ID)
            data = get_guild_data_r(guild.id)
        except Exception as e:
            raise Exception from e
        data["events"][event_id] = {
            "id": event_id,
            "title": title,
            "dateUnix": unix_ts,
            "rosterId": roster_id,
            "createdBy": str(interaction.user.id),
            "pinged": False,
            "linkedDiscordEventId": None,
        }
        set_guild_data_r(guild.id, data)
        await interaction.response.send_message(
            "Successfully completed operation /cevent ✅", ephemeral=True
        )

    @app_commands.command(name="delete-event", description="Delete an event")
    async def delete_event(self, interaction: discord.Interaction, event_id: str) -> None:
        """Handles the /devent command"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data_r(GUILD_ID)
        if event_id in data["events"]:
            del data["events"][event_id]
            set_guild_data_r(GUILD_ID, data)
            await interaction.response.send_message(
                f"🗑️ Event {event_id} deleted.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Event not found.", ephemeral=True
            )

    @app_commands.command(name="edit-event", description="Edit an event")
    async def edit_event(
        self,
        interaction: discord.Interaction,
        event_id: str,
        new_title: Optional[str] = None,
        new_unix_time: Optional[int] = None,
    ) -> None:
        """Handles the /eevent command"""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data_r(GUILD_ID)
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
        set_guild_data_r(GUILD_ID, data)
        await interaction.response.send_message(
            f"✏️ Event {event_id} updated.", ephemeral=True
        )

    @app_commands.command(
        name="link-event", description="Link a FootBot event to a Discord Scheduled Event"
    )
    async def link_event(
        self, interaction: discord.Interaction, event_id: str, discord_event_id: int
    ) -> None:
        """Link a FootBot event to a Discord Scheduled Event by ID."""
        if not validate_permissions_r(interaction):
            await interaction.response.send_message(
                "You do not have access to this command!", ephemeral=True
            )
            return
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data_r(GUILD_ID)
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
        set_guild_data_r(GUILD_ID, data)

        await interaction.response.send_message(
            f"🔗 Linked FootBot event {event_id} to Discord event {scheduled_event.name}.",
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot"""
    command_list_add(Events.create_event.name)
    command_list_add(Events.edit_event.name)
    command_list_add(Events.delete_event.name)
    command_list_add(Events.link_event.name)
    await bot.add_cog(Events(bot))
