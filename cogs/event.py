import discord
from discord.ext import commands
from discord import app_commands
from typing import Any, Dict, Optional
from utils.storage import get_guild_data, set_guild_data
from utils.validator import validate_interaction_guild


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="cevent", description="Create an event")
    async def cevent(
        self,
        interaction: discord.Interaction,
        event_id: str,
        title: str,
        unix_time: int,
        roster_id: Optional[str] = None,
    ) -> None:
        guild = validate_interaction_guild(interaction)
        GUILD_ID = guild.id
        data: Dict[str, Any] = get_guild_data(GUILD_ID)
        data["events"][event_id] = {
            "id": event_id,
            "title": title,
            "dateUnix": unix_time,
            "rosterId": roster_id,
            "createdBy": str(interaction.user.id),
            "pinged": False,
        }
        set_guild_data(GUILD_ID, data)
        await interaction.response.send_message(
            f"✅ Event {title} created for <t:{unix_time}:F>.", ephemeral=True
        )

    @app_commands.command(name="devent", description="Delete an event")
    async def devent(self, interaction: discord.Interaction, event_id: str) -> None:
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

    @app_commands.command(name="eevent", description="Edit an event title or time")
    async def eevent(
        self,
        interaction: discord.Interaction,
        event_id: str,
        new_title: Optional[str] = None,
        new_unix_time: Optional[int] = None,
    ) -> None:
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
