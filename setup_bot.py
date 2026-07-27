from typing import Any
import discord
from discord import app_commands
from discord.ext import commands
from utils.storage import command_list_add, MAIN

class SubBotSelect(discord.ui.Select[Any]):
    """The Sub bot selector"""
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Roster",
                description="Invite the Roster bot"
            ),
            discord.SelectOption(
                label="Leaderboard",
                description="Invite the Leaderboard bot"
            ),
        ]

        super().__init__(
            placeholder="Choose a bot to invite",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        """The callback"""
        choice = self.values[0]

        INVITES:dict[str, str|list[str]] = {
            "Roster": "https://discord.com/oauth2/authorize?client_id=ROSTER_BOT_ID&scope=bot%20applications.commands&permissions=2147483647",
            "Leaderboard": "https://discord.com/oauth2/authorize?client_id=LEADERBOARD_BOT_ID&scope=bot%20applications.commands&permissions=2147483647",
        }

        invite = INVITES[choice]

        embed = discord.Embed(
            title=f"{choice} Bot",
            description=f"[Click here to invite the {choice} bot]({invite})",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


class SubBotView(discord.ui.View):
    """The view of the selectmenu"""
    def __init__(self):
        super().__init__()
        self.add_item(SubBotSelect())
class SetupBot(commands.Cog):
    """The command class"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="setup-bot", description="Invite the sub-bots.")
    async def setup_bot(self, interaction: discord.Interaction):
        """Sends the invite in a clean embed"""
        await interaction.response.send_message(
            "Select which bot you want to invite:",
            view=SubBotView(),
            ephemeral=True
        )
async def setup(bot: commands.Bot):
    """Perpares the bot"""
    command_list_add("", MAIN)
    await bot.add_cog(SetupBot(bot))
