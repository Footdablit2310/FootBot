"""Scheduling"""

import datetime
from typing import Any, Dict
import pytz
from discord.ext import tasks, commands
from utils.storage import load_all, save_all, set_guild_data


def start_scheduler(bot: commands.Bot) -> None:
    """Starts the scheduler"""

    @tasks.loop(seconds=30.0, name="Check events")
    async def check_events() -> None:
        now: int = int(datetime.datetime.now(pytz.utc).timestamp())
        all_data: Dict[str, Dict[str, dict[str, Any]]] = load_all()
        for guild_id, guild_data in all_data.items():
            ping_minutes: int = int(guild_data["config"].get("pingMinutesBefore", 15))
            threshold: int = ping_minutes * 60
            for ev in guild_data["events"].copy().values():
                if ev["dateUnix"] <= now:
                    event_id = ev["id"]
                    if event_id in guild_data["events"]:
                        del guild_data["events"][event_id]
                        set_guild_data(int(guild_id), guild_data)
                        print("✅🗑️ Old event deleted.")
                    else:
                        print("❌🗑️ Old event not found.")
                if ev.get("pinged"):
                    continue
                if 0 <= (ev["dateUnix"] - now) <= threshold:
                    guild = bot.get_guild(int(guild_id))
                    if guild is None:
                        continue
                    channel_id: str | None = guild_data["config"].get("eventChannelId")
                    if channel_id is None:
                        continue
                    channel = guild.get_channel(
                        int(channel_id.removeprefix("<#").removesuffix(">"))
                    )
                    if channel is None:
                        continue
                    roster: Dict[str, Any] | None = guild_data["rosters"].get(
                        ev.get("rosterId")
                    )
                    role_mention: str = (
                        f"<@&{roster['roleId']}>"
                        if roster and roster.get("roleId")
                        else ""
                    )
                    await channel.send(f"🔔 Reminder: Event **{ev['title']}** starts soon! {role_mention}")  # type: ignore
                    ev["pinged"] = True
        save_all(all_data)

    check_events.start()
