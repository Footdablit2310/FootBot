"""Minecraft server configuration cog."""

from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from utils.validator import validate_interaction_guild, check_if_owner
from utils.storage import (
    MCLINK_DATA_FILE,
    load_json_file,
    save_json_file,
)

# ── Strict-mode type aliases ─────────────────────────────────────────────────
type ServerConfig = dict[str, str]
type GuildServers = dict[str, ServerConfig]
type MCFileData = dict[str, GuildServers]


class MinecraftConfig(commands.Cog):
    """Owner-only commands to manage Minecraft server links per guild."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ── Helper: safe ephemeral reply ─────────────────────────────────────────
    async def _reply(
        self,
        interaction: discord.Interaction,
        message: str,
    ) -> None:
        """Send an ephemeral reply, handling already-responded interactions."""
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)

    # ── Helper: load data safely ─────────────────────────────────────────────
    def _load_data(self) -> MCFileData:
        """Load the MC data file. Raises RuntimeError if unreadable."""
        raw: object = load_json_file(MCLINK_DATA_FILE)
        if not isinstance(raw, dict):
            raise RuntimeError("MCLINK_DATA_FILE is missing or corrupted")
        return raw  # type: ignore[return-value]

    # ── add_server ───────────────────────────────────────────────────────────
    @app_commands.command(
        name="add_server",
        description="Add a new Minecraft server to this guild",
    )
    @app_commands.guild_only()
    @app_commands.check(check_if_owner)
    @app_commands.describe(
        server_name="Unique display name for this server",
        server_ip="Server IP address or hostname",
        port="Server port (1-65535)",
    )
    async def add_server(
        self,
        interaction: discord.Interaction,
        server_name: str,
        server_ip: str,
        port: app_commands.Range[int, 1, 65535],
    ) -> None:
        """Add an additional server. Duplicate names are rejected."""
        guild: discord.Guild = validate_interaction_guild(interaction)
        guild_id: str = str(guild.id)

        data: MCFileData = self._load_data()

        guild_servers: GuildServers | None = data.get(guild_id)
        if guild_servers is None:
            await self._reply(
                interaction,
                "❌ Guild has no MC data. Run `/setup-mc` first.",
            )
            return

        if server_name in guild_servers:
            await self._reply(
                interaction,
                f"❌ A server named **{server_name}** already exists.",
            )
            return

        server_cfg: ServerConfig = {
            "name": server_name,
            "IP": server_ip,
            "port": str(port),
        }
        guild_servers[server_name] = server_cfg
        save_json_file(MCLINK_DATA_FILE, data)

        await self._reply(
            interaction,
            f"✅ Server **{server_name}** (`{server_ip}:{port}`) added.",
        )

    # ── remove_server ────────────────────────────────────────────────────────
    @app_commands.command(
        name="remove_server",
        description="Remove a Minecraft server from this guild",
    )
    @app_commands.guild_only()
    @app_commands.check(check_if_owner)
    @app_commands.describe(server_name="Exact name of the server to remove")
    async def remove_server(
        self,
        interaction: discord.Interaction,
        server_name: str,
    ) -> None:
        """Remove a server. Deleting the last remaining server is blocked."""
        guild: discord.Guild = validate_interaction_guild(interaction)
        guild_id: str = str(guild.id)

        data: MCFileData = self._load_data()

        guild_servers: GuildServers | None = data.get(guild_id)
        if guild_servers is None:
            await self._reply(interaction, "❌ This guild has no MC data.")
            return

        if server_name not in guild_servers:
            await self._reply(
                interaction,
                f"❌ Server **{server_name}** not found.",
            )
            return

        if len(guild_servers) <= 1:
            await self._reply(
                interaction,
                "❌ Cannot delete the last server. Use `/delete_guild_data` to wipe everything.",
            )
            return

        del guild_servers[server_name]
        save_json_file(MCLINK_DATA_FILE, data)

        await self._reply(interaction, f"✅ Server **{server_name}** removed.")

    # ── delete_guild_data ────────────────────────────────────────────────────
    @app_commands.command(
        name="delete_guild_data",
        description="Permanently delete all Minecraft data for this guild",
    )
    @app_commands.guild_only()
    @app_commands.check(check_if_owner)
    async def delete_guild_data(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """Nuke the entire guild entry from the MC data file."""
        guild: discord.Guild = validate_interaction_guild(interaction)
        guild_id: str = str(guild.id)

        data: MCFileData = self._load_data()

        if guild_id not in data:
            await self._reply(
                interaction,
                "❌ No MC data exists for this guild.",
            )
            return

        del data[guild_id]
        save_json_file(MCLINK_DATA_FILE, data)

        await self._reply(
            interaction,
            "✅ All Minecraft data for this guild has been deleted.",
        )

    # ── Error handler for owner checks ───────────────────────────────────────
    @add_server.error
    @remove_server.error
    @delete_guild_data.error
    async def on_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, app_commands.CheckFailure):
            await self._reply(
                interaction,
                "You must be the server owner to run this command!",
            )
            return
        raise error


async def setup(bot: commands.Bot) -> None:
    """Add the MinecraftConfig cog to the bot."""
    await bot.add_cog(MinecraftConfig(bot))