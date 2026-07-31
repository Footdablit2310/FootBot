"""Setup handler"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.validator import validate_interaction_guild
from utils.storage import load_json_file, save_json_file, MCLINK_DATA_FILE


class Config(commands.Cog):
    """The config class"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="setup-mc",
        description="The Setup function which sets up your mc server system",
    )
    @app_commands.default_permissions(discord.permissions.Permissions.all())
    async def setup_mc(self, interaction: discord.Interaction, server_name:str, server_ip:str, port:int):
        """The setup system for the minecraft suite"""
        guild = validate_interaction_guild(interaction)
        if not interaction.user.id == guild.owner_id:
            await interaction.response.send_message("You must be the server owner to run this command!")
            return
        try:
            data:dict[str, dict[str, str]|None]|None=load_json_file(MCLINK_DATA_FILE)
            if data is None:
                raise RuntimeError
            validation_data=data[str(guild.id)]
            if validation_data is None:
                raise ValueError
            await interaction.response.send_message("ERROR: MC already setup!")

        except ValueError:
            guild_data:dict[str, str] = {
                "name":server_name,
                "IP":server_ip,
                "port":str(port)
            }
            data:dict[str, dict[str, str]|None]|None=load_json_file(MCLINK_DATA_FILE)
            if data is None:
                raise RuntimeError
            data[str(guild.id)] = guild_data
            save_json_file(MCLINK_DATA_FILE, data)
            await interaction.response.send_message("✅Setup is successfull!")
