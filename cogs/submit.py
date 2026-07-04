"""Submit Cog Handler"""
from typing import Dict, Any, List
import discord
from discord import app_commands
from discord.ext import commands
from utils.storage import get_guild_data_l, set_guild_data_l
from utils.validator import validate_permissions_l, validate_interaction_guild, can_access_role

#pylint: disable=W0718
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
        Validation happens as early as reasonably possible:
         - ensure command run in a guild
         - ensure maps exist
         - ensure completed structure exists
         - filter out maps the user already completed
         - filter out maps the user cannot access by rank
        """
        # Must be run in a guild
        guild = validate_interaction_guild(interaction)

        # Build proof value
        if attachment:
            proof_value: str = f"{attachment.url}"
        elif proof:
            proof_value = f"{proof}"
        else:
            await interaction.response.send_message("Provide proof as text or file.", ephemeral=True)
            return

        # Load guild data and ensure structures exist
        guild_data: Dict[str, Any] = get_guild_data_l(guild.id)
        maps_data: List[Dict[str, Any]] = guild_data.get("maps", [])
        if "completed" not in guild_data:
            guild_data["completed"] = {}
        completed: Dict[str, List[str]] = guild_data.get("completed", {})

        if not maps_data:
            await interaction.response.send_message("No maps available to select.", ephemeral=True)
            return

        # Ensure caller is a Member (not a DM user)
        member = interaction.user
        if isinstance(member, discord.User):
            await interaction.response.send_message("You must run this command from a server (guild) channel.", ephemeral=True)
            return

        member_id_str = str(member.id)
        member_completed = set(completed.get(member_id_str, []))

        # Filter out maps the member already completed
        not_completed_maps = [m for m in maps_data if m["name"] not in member_completed]
        if not not_completed_maps:
            await interaction.response.send_message("You have already completed all available maps.", ephemeral=True)
            return

        # Filter out maps the member cannot access by rank (early validation)
        accessible_maps: List[Dict[str, Any]] = []
        for m in not_completed_maps:
            role_required = guild.get_role(m["role_required"])
            # If role is missing from guild, skip it
            if role_required is None:
                continue
            # can_access_role should return True if member can submit/view maps for that role
            try:
                allowed = can_access_role(interaction, role_required)
            except Exception:
                # If validator raises, treat as not allowed
                allowed = False
            if allowed:
                accessible_maps.append(m)

        if not accessible_maps:
            await interaction.response.send_message(
                "There are no maps you can submit for right now (either all completed or above your rank).",
                ephemeral=True
            )
            return

        # Build rank list dynamically from accessible maps
        ranks: List[str] = sorted({m["difficulty"] for m in accessible_maps})
        maps_by_rank: Dict[str, List[Dict[str, Any]]] = {
            rank: [m for m in accessible_maps if m["difficulty"] == rank] for rank in ranks
        }

        view: RankMapSelectView = RankMapSelectView(proof_value, member, maps_by_rank, guild.id)
        await interaction.response.send_message("Select rank and map:", view=view, ephemeral=True)


class RankMapSelectView(discord.ui.View):
    """Rank select menu"""
    def __init__(self, proof_value: str, submitter: discord.Member,
                 maps_by_rank: Dict[str, List[Dict[str, Any]]], guild_id: int) -> None:
        super().__init__(timeout=60)
        self.proof_value = proof_value
        self.submitter = submitter
        self.maps_by_rank = maps_by_rank
        self.guild_id = guild_id

        if not maps_by_rank:
            return

        options = [discord.SelectOption(label=rank) for rank in maps_by_rank.keys()]
        if not options:
            return

        select:discord.ui.Select[Any] = discord.ui.Select(
            placeholder="Choose Rank",
            options=options,
        )

        async def on_rank_select(interaction: discord.Interaction):
            rank = select.values[0]
            maps = self.maps_by_rank[rank]
            if not maps:
                await interaction.response.send_message("No maps for this rank.", ephemeral=True)
                return

            map_options = [discord.SelectOption(label=m["name"]) for m in maps]
            view = MapSelectView(self.proof_value, self.submitter, rank, maps, self.guild_id)

            map_select:discord.ui.Select[Any] = discord.ui.Select(
                placeholder="Choose Map",
                options=map_options,
            )

            async def on_map_select(interaction: discord.Interaction):
                mapname = map_select.values[0]
                chosen_map = next(m for m in maps if m["name"] == mapname)
                embed = discord.Embed(
                    title=f"{mapname} ({rank})",
                    description=f"Proof: {self.proof_value}",
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Submitted by {self.submitter.display_name}")
                channel = interaction.channel
                if channel is None:
                    await interaction.response.send_message("Must be run from guild")
                    raise ValueError("Must be run from guild")
                await channel.send( # type: ignore
                    embed=embed,
                    view=ApprovalView(chosen_map, self.proof_value, self.submitter, self.guild_id)
                )
                await interaction.response.edit_message(content="Submission posted.", view=None)

            map_select.callback = on_map_select
            view.add_item(map_select)
            await interaction.response.edit_message(content=f"Rank chosen: {rank}. Now select a map:", view=view)

        select.callback = on_rank_select
        self.add_item(select)




class MapSelectView(discord.ui.View):
    """The map select"""
    def __init__(self, proof_value: str, submitter: discord.Member,
                 rank: str, maps: List[Dict[str, Any]], guild_id: int) -> None:
        super().__init__(timeout=60)
        self.proof_value = proof_value
        self.submitter = submitter
        self.rank = rank
        self.maps = maps
        self.guild_id = guild_id

        if not maps:  # guard against empty maps list
            return

        options = [discord.SelectOption(label=m["name"]) for m in maps]
        if not options:
            return

        self.add_item(discord.ui.Select(
            placeholder="Choose Map",
            options=options,
        ))


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
        Approve submission, award points if permissions validated, and mark completed early.
        """
        if not validate_permissions_l(interaction):
            await interaction.response.send_message("You don’t have permission to approve.", ephemeral=True)
            return

        guild_data: Dict[str, Any] = get_guild_data_l(self.guild_id)

        # Leaderboard update
        leaderboard: List[Dict[str, int]] = guild_data.get("leaderboard", [])
        lb_dict: Dict[str, int] = {}
        for entry in leaderboard:
            lb_dict.update(entry)

        user_id: str = str(self.submitter.id)
        lb_dict[user_id] = lb_dict.get(user_id, 0) + self.map_entry["points"]
        guild_data["leaderboard"] = [{uid: pts} for uid, pts in lb_dict.items()]

        # Completed update (prevent resubmission)
        completed: Dict[str, List[str]] = guild_data.get("completed", {})
        if user_id not in completed:
            completed[user_id] = []
        if self.map_entry["name"] not in completed[user_id]:
            completed[user_id].append(self.map_entry["name"])
        guild_data["completed"] = completed
        # Persist changes
        set_guild_data_l(self.guild_id, guild_data)
        await interaction.message.delete() # type: ignore
        await interaction.response.send_message(
            f"✅ Approved! {self.submitter.mention} gains {self.map_entry['points']} points. "
            f"Map **{self.map_entry['name']}** marked as completed.",
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
        await interaction.message.delete() #type: ignore
        await interaction.response.send_message("❌ Submission denied.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Prepares the Bot by adding the Submit Cog."""
    await bot.add_cog(Submit(bot))

#pylint: enable=W0718
