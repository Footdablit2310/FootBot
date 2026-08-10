"""Setup handler"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.validator import validate_interaction_guild, check_if_owner
from utils.storage import load_json_file, save_json_file, MCLINK_DATA_FILE


class SetupMC(commands.Cog):
    """The setup class"""

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

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="setup-mc",
        description="The Setup function which sets up your mc server system",
    )
    @app_commands.check(check_if_owner)
    async def setup_mc(
        self,
        interaction: discord.Interaction,
        server_name: str,
        server_ip: str,
        port: int,
    ):
        """The setup system for the minecraft suite"""
        guild = validate_interaction_guild(interaction)
        if not interaction.user == guild.owner:
            await interaction.response.send_message(
                "You must be the server owner to run this command!"
            )
            return
        data: dict[str, dict[str, dict[str, str]] | None] | None = load_json_file(
            MCLINK_DATA_FILE
        )
        try:
            if data is None:
                raise RuntimeError
            validation_data = data[str(guild.id)]
            if validation_data is None:
                raise ValueError
            await interaction.response.send_message("ERROR: MC already setup!")

        except ValueError:
            guild_data: dict[str, dict[str, str]] = {
                server_name: {"name": server_name, "IP": server_ip, "port": str(port)}
            }
            if data is None:
                raise RuntimeError
            data[str(guild.id)] = guild_data
            save_json_file(MCLINK_DATA_FILE, data)
            await interaction.response.send_message("✅Setup is successfull!")
    @setup_mc.error
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


async def setup(bot: commands.Bot):
    await bot.add_cog(SetupMC(bot))
