"""Submit Cog Handler"""
from typing import Dict, Any, List
import discord
from discord import app_commands
from discord.ext import commands
from utils.storage import get_guild_data_l
from utils.validator import validate_permissions_l, validate_interaction_guild



class Submit(commands.Cog):
    """
    Cog providing the /submit command for map completions.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="submit", description="Submit proof of completion")
    @app_commands.describe(
        proof="Proof as text (URL)",
        attachment="Upload proof file"
    )
    async def submit(
        self,
        interaction: discord.Interaction,
        proof: str | None = None,
        attachment: discord.Attachment | None = None
    ) -> None:
        """
        Slash command to submit proof of completion.
        Accepts either a text URL or an uploaded file.
        """
        guild=validate_interaction_guild(interaction)
        if attachment:
            proof_value: str = f"[File]({attachment.url})"
        elif proof:
            proof_value = f"[Proof]({proof})"
        else:
            await interaction.response.send_message("Provide proof as text or file.", ephemeral=True)
            return

        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        maps_data: List[Dict[str, Any]] = guild_data["maps"]

        if not maps_data:
            await interaction.response.send_message("No maps available to select.", ephemeral=True)
            return
        member=interaction.user
        if isinstance(member, discord.User):
            await interaction.response.send_message("YOU MUST RUN THIS FROM A GUILD!")
        else:
            # Build rank list dynamically from maps
            ranks: List[str] = sorted(set(m["difficulty"] for m in maps_data))
            maps_by_rank: Dict[str, List[Dict[str, Any]]] = {rank: [m for m in maps_data if m["difficulty"] == rank] for rank in ranks}

            view: RankMapSelectView = RankMapSelectView(proof_value, member, maps_by_rank, guild.id)
            await interaction.response.send_message("Select rank and map:", view=view, ephemeral=True)


class RankMapSelectView(discord.ui.View):
    """
    First step view: select rank, then map.
    """

    def __init__(self, proof_value: str, submitter: discord.Member, maps_by_rank: Dict[str, List[Dict[str, Any]]], guild_id: int) -> None:
        super().__init__(timeout=60)
        self.proof_value: str = proof_value
        self.submitter: discord.Member = submitter
        self.maps_by_rank: Dict[str, List[Dict[str, Any]]] = maps_by_rank
        self.guild_id: int = guild_id

        self.add_item(discord.ui.Select(
            placeholder="Choose Rank",
            options=[discord.SelectOption(label=rank) for rank in maps_by_rank.keys()],
            custom_id="rank_select"
        ))

    @discord.ui.select(custom_id="rank_select")
    async def rank_select(self, interaction: discord.Interaction, select: discord.ui.Select[Any]) -> None:
        """
        Handle rank selection, then show map options.
        """
        rank: str = select.values[0]
        maps: List[Dict[str, Any]] = self.maps_by_rank[rank]
        map_options: List[discord.SelectOption] = [discord.SelectOption(label=m["name"]) for m in maps]

        view: MapSelectView = MapSelectView(self.proof_value, self.submitter, rank, maps, self.guild_id)
        view.add_item(discord.ui.Select(placeholder="Choose Map", options=map_options, custom_id="map_select"))
        await interaction.response.edit_message(content=f"Rank chosen: {rank}. Now select a map:", view=view)


class MapSelectView(discord.ui.View):
    """
    Second step view: select map, then post embed with Approve/Deny.
    """

    def __init__(self, proof_value: str, submitter: discord.Member, rank: str, maps: List[Dict[str, Any]], guild_id: int) -> None:
        super().__init__(timeout=60)
        self.proof_value: str = proof_value
        self.submitter: discord.Member = submitter
        self.rank: str = rank
        self.maps: List[Dict[str, Any]] = maps
        self.guild_id: int = guild_id

    @discord.ui.select(custom_id="map_select")
    async def map_select(self, interaction: discord.Interaction, select: discord.ui.Select[Any]) -> None:
        """
        Handle map selection, then post public embed with Approve/Deny.
        """
        mapname: str = select.values[0]
        chosen_map: Dict[str, Any] = next(m for m in self.maps if m["name"] == mapname)

        embed: discord.Embed = discord.Embed(
            title=f"{mapname} ({self.rank})",
            description=f"Proof: {self.proof_value}",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Submitted by {self.submitter.display_name}")
        if interaction.channel is None:
            await interaction.response.send_message("Could not respond: Invalid run location!")
        else:
            await interaction.channel.send(embed=embed, view=ApprovalView(chosen_map, self.proof_value, self.submitter, self.guild_id)) # type: ignore
            await interaction.response.edit_message(content="Submission posted.", view=None)


class ApprovalView(discord.ui.View):
    """
    Final view: Approve or Deny submission.
    """

    def __init__(self, map_entry: Dict[str, Any], proof_value: str, submitter: discord.Member, guild_id: int) -> None:
        super().__init__(timeout=None)
        self.map_entry: Dict[str, Any] = map_entry
        self.proof_value: str = proof_value
        self.submitter: discord.Member = submitter
        self.guild_id: int = guild_id

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button[Any]) -> None:
        """
        Approve submission, award points if permissions validated.
        """
        if not validate_permissions_l(interaction):
            await interaction.response.send_message("You don’t have permission to approve.", ephemeral=True)
            return

        guild_data: Dict[str, Any] = get_guild_data_l(self.guild_id)
        leaderboard: List[Dict[str, int]] = guild_data["leaderboard"]

        # Flatten leaderboard
        lb_dict: Dict[str, int] = {}
        for entry in leaderboard:
            lb_dict.update(entry)

        # Award points
        user_id: str = str(self.submitter.id)
        lb_dict[user_id] = lb_dict.get(user_id, 0) + self.map_entry["points"]

        # Rebuild leaderboard as list of dicts
        guild_data["leaderboard"] = [{uid: pts} for uid, pts in lb_dict.items()]
        await interaction.response.send_message(
            f"✅ Approved! {self.submitter.mention} gains {self.map_entry['points']} points.",
            ephemeral=True
        )

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button[Any]) -> None:
        """
        Deny submission, no points awarded.
        """
        if not validate_permissions_l(interaction):
            await interaction.response.send_message("You don’t have permission to deny.", ephemeral=True)
            return

        await interaction.response.send_message("❌ Submission denied.", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot by adding the Map Cog."""
    await bot.add_cog(Submit(bot))