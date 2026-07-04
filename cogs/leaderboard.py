"""Leaderboard Cog for Discord Bot"""
from typing import Dict, Any, List, Tuple
import discord
from discord import app_commands
from discord.ext import commands
from utils.storage import get_guild_data_l
from utils.validator import validate_interaction_guild
class LeaderboardView(discord.ui.View):
    """
    Interactive view for paginated leaderboard.
    Provides Next/Prev buttons to navigate pages.
    """

    def __init__(self, guild: discord.Guild, leaderboard: List[Dict[str, int]], page: int = 0) -> None:
        super().__init__(timeout=None)
        self.guild: discord.Guild = guild
        self.leaderboard: List[Dict[str, int]] = leaderboard
        self.page: int = page
        self.per_page: int = 24

    def _flatten_leaderboard(self) -> Dict[str, int]:
        """
        Flatten the leaderboard list of dicts into a single dict.
        """
        lb_dict: Dict[str, int] = {}
        for entry in self.leaderboard:
            lb_dict.update(entry)
        return lb_dict

    def make_embed(self) -> discord.Embed:
        """
        Build the leaderboard embed for the current page.
        """
        lb_dict: Dict[str, int] = self._flatten_leaderboard()
        sorted_lb: List[Tuple[str, int]] = sorted(lb_dict.items(), key=lambda x: x[1], reverse=True)
        total_pages: int = (len(sorted_lb) - 1) // self.per_page + 1

        start: int = self.page * self.per_page
        end: int = start + self.per_page
        entries: List[Tuple[str, int]] = sorted_lb[start:end]

        embed: discord.Embed = discord.Embed(
            title=f"Leaderboard — Page {self.page+1}/{total_pages}",
            color=discord.Color.gold()
        )

        for idx, (user_id, points) in enumerate(entries, start=start+1):
            member: discord.Member | None = self.guild.get_member(int(user_id))
            if member is None:
                raise ValueError("Must be ran from a guild")
            mention: str = member.mention
            embed.add_field(
                name="",
                value=f"**#{idx}:** {mention} {points} points",
            )

        return embed

    @discord.ui.button(label="Prev", style=discord.ButtonStyle.secondary)
    async def prev_page(self, interaction: discord.Interaction, button: discord.ui.Button[Any]) -> None:
        """
        Navigate to the previous page if available.
        """
        if self.page > 0:
            self.page -= 1
            await interaction.response.edit_message(embed=self.make_embed(), view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button[Any]) -> None:
        """
        Navigate to the next page if available.
        """
        lb_dict: Dict[str, int] = self._flatten_leaderboard()
        sorted_lb: List[Tuple[str, int]] = sorted(lb_dict.items(), key=lambda x: x[1], reverse=True)

        if (self.page + 1) * self.per_page < len(sorted_lb):
            self.page += 1
            await interaction.response.edit_message(embed=self.make_embed(), view=self)


class Leaderboard(commands.Cog):
    """
    Cog providing the /leaderboard command with pagination.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="leaderboard", description="Show leaderboard with pagination")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        """
        Slash command to display the guild leaderboard.
        """
        guild=validate_interaction_guild(interaction)
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        leaderboard: List[Dict[str, int]] = guild_data["leaderboard"]

        if not leaderboard:
            await interaction.response.send_message("Leaderboard is empty.", ephemeral=True)
            return

        view: LeaderboardView = LeaderboardView(guild, leaderboard, page=0)
        await interaction.response.send_message(embed=view.make_embed(), view=view)


async def setup(bot: commands.Bot) -> None:
    """
    Setup function to add the Leaderboard cog.
    """
    await bot.add_cog(Leaderboard(bot))
