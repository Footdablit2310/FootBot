"""Scheduling"""
import datetime
from typing import Any, Dict
import requests
import pytz
from discord.ext import tasks, commands
from mcrcon import MCRcon
from utils.storage import load_all_r, save_all_r, set_guild_data_r, load_mc

def start_scheduler(bot: commands.Bot) -> None:
    """Starts the scheduler"""

    @tasks.loop(seconds=30.0, name="Check events")
    async def check_events() -> None:
        now: int = int(datetime.datetime.now(pytz.utc).timestamp())
        all_data: Dict[str, Dict[str, dict[str, Any]]] = load_all_r()
        for guild_id, guild_data in all_data.items():
            ping_minutes: int = int(guild_data["config"].get("pingMinutesBefore", 15))
            threshold: int = ping_minutes * 60
            for ev in guild_data["events"].copy().values():
                if ev["dateUnix"] <= now:
                    event_id = ev["id"]
                    if event_id in guild_data["events"]:
                        del guild_data["events"][event_id]
                        set_guild_data_r(int(guild_id), guild_data)
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
        save_all_r(all_data)
    @tasks.loop(seconds=60.0, name="Sync whitelist to minecraft server")
    async def sync_whitelist() -> None:
        """Background task to sync whitelists for all guilds."""
        data: Dict[str, Any] = load_mc()
        for guild_id, guild_data in data.get("guilds", {}).items():
            rcon_info = guild_data.get("rcon", {})
            host = rcon_info.get("host")
            port = rcon_info.get("port")
            password = rcon_info.get("password")

            if not host or not password:
                continue  # skip guilds without setup
            #pylint: disable=W0718
            try:
                with MCRcon(host, password, port=port) as mcr: # type: ignore
                    for accounts in guild_data.get("links", {}).values():
                        for username in accounts:
                            uuid = get_uuid(username)
                            if uuid:
                                mcr.command(f"/whitelist add {username}") #type: ignore
            except Exception as e:
                print(f"[Scheduler] Error syncing guild {guild_id}: {e}")
            #pylint: enable=W0718
    sync_whitelist.start()
    check_events.start()

def get_uuid(username: str) -> str | None:
    """Resolve Minecraft username to UUID via Mojang API."""
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json().get("id")
    except requests.RequestException:
        return None
    return None
