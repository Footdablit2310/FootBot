"""Linking system"""
from typing import Any, Dict
import discord
from discord import app_commands
from discord.ext import commands
from utils.storage import load_mc, save_mc, get_guild_data_mc, MC_FILE, command_list_add
from utils.validator import has_permissions_mc, check_for_guild_data, validate_interaction_guild

class MCCommands(commands.Cog):
    """Minecraft commands"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="link_mc")
    async def link_mc(self, ctx: commands.Context[Any], minecraft_username: str) -> None:
        """Links user"""
        guild=ctx.guild
        if guild is None:
            raise ValueError
        if not check_for_guild_data(MC_FILE, guild):
            await ctx.send("Use /setup-mc first, there is no guild data")
            return
        member=ctx.author
        if isinstance(member, discord.User):
            raise TypeError("Can not be run from DM")
        if not has_permissions_mc(member):
            await ctx.send("❌ You don’t have permission.")
            return

        data: Dict[str, Any] = load_mc()
        accounts = data["links"].get(str(ctx.author.id), [])
        if minecraft_username not in accounts:
            accounts.append(minecraft_username)
            data["links"][str(ctx.author.id)] = accounts
            save_mc(data)
            await ctx.send(f"✅ Linked `{minecraft_username}` to {ctx.author.mention}.")
        else:
            await ctx.send("⚠️ Already linked.")

    @commands.command(name="unlink_mc")
    async def unlink_mc(self, ctx: commands.Context[Any], minecraft_username: str) -> None:
        """Unlinks user"""
        member=ctx.author
        if isinstance(member, discord.User):
            raise TypeError("Can not be run from DM")
        if not has_permissions_mc(member):
            await ctx.send("❌ You don’t have permission.")
            return

        data: Dict[str, Any] = load_mc()
        accounts = data["links"].get(str(ctx.author.id), [])
        if minecraft_username in accounts:
            accounts.remove(minecraft_username)
            data["links"][str(ctx.author.id)] = accounts
            save_mc(data)
            await ctx.send(f"✅ Unlinked `{minecraft_username}`.")
        else:
            await ctx.send("⚠️ That account isn’t linked.")

    @commands.command(name="add_permissions_mc")
    @commands.has_guild_permissions(administrator=True)
    async def add_permissions_mc(
        self, ctx: commands.Context[Any], member: discord.Member | None = None, role: discord.Role | None = None
    ) -> None:
        """Adds permissions"""
        data: Dict[str, Any] = load_mc()
        if member:
            if str(member.id) not in data["permissions"]["users"]:
                data["permissions"]["users"].append(str(member.id))
                await ctx.send(f"✅ Added user {member.mention} to MC permissions.")
        if role:
            if role.name not in data["permissions"]["roles"]:
                data["permissions"]["roles"].append(role.name)
                await ctx.send(f"✅ Added role `{role.name}` to MC permissions.")
        save_mc(data)

    @commands.command(name="remove_permissions_mc")
    @commands.has_guild_permissions(administrator=True)
    async def remove_permissions_mc(
        self, ctx: commands.Context[Any], member: discord.Member | None = None, role: discord.Role | None = None
    ) -> None:
        """Removes permissions"""
        data: Dict[str, Any] = load_mc()
        if member and str(member.id) in data["permissions"]["users"]:
            data["permissions"]["users"].remove(str(member.id))
            await ctx.send(f"❌ Removed user {member.mention} from MC permissions.")
        if role and role.name in data["permissions"]["roles"]:
            data["permissions"]["roles"].remove(role.name)
            await ctx.send(f"❌ Removed role `{role.name}` from MC permissions.")
        save_mc(data)

class RconConfig(commands.Cog):
    """Handles RCON"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="rcon", description="View or update RCON configuration")
    async def rcon(
        self,
        interaction: discord.Interaction,
        host: str | None = None,
        port: int | None = None,
        password: str | None = None
    ) -> None:
        """RCON"""
        guild=validate_interaction_guild(interaction)
        # Only guild owner can run
        if interaction.user.id != guild.owner_id:
            await interaction.response.send_message("❌ Only the guild owner can run this command.", ephemeral=True)
            return

        data: Dict[str, Any] = load_mc()
        guild_data = get_guild_data_mc(guild.id)

        # If no params → show current config
        if host is None and port is None and password is None:
            rcon_info = guild_data["rcon"]
            masked_pw = "●" * len(rcon_info["password"]) if rcon_info["password"] else "(not set)"
            await interaction.response.send_message(
                f"🔧 Current RCON configuration:\n"
                f"Host: `{rcon_info['host']}`\n"
                f"Port: `{rcon_info['port']}`\n"
                f"Password: `{masked_pw}`",
                ephemeral=True
            )
            return

        # Update values if provided
        if host is not None:
            guild_data["rcon"]["host"] = host
            await interaction.followup.send("Updated rcon host")
        if port is not None:
            guild_data["rcon"]["port"] = port
            await interaction.followup.send("Updated rcon port")
        if password is not None:
            guild_data["rcon"]["password"] = password
            await interaction.followup.send("Updated rcon password")
        data["guilds"][str(interaction.guild_id)] = guild_data
        save_mc(data)

        await interaction.response.send_message("✅ RCON configuration updated.", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    """Prepares the bot"""
    command_list_add(RconConfig.rcon.name)
    command_list_add(MCCommands.link_mc.name)
    command_list_add(MCCommands.unlink_mc.name)
    command_list_add(MCCommands.add_permissions_mc.name)
    command_list_add(MCCommands.remove_permissions_mc.name)
    await bot.add_cog(MCCommands(bot))
    await bot.add_cog(RconConfig(bot))