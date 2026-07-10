"""The file with Validator Utils"""

from typing import Any
from discord import Interaction, Guild, Role, User, Member
from utils.storage import get_guild_data_r, get_guild_data_l, load_mc, load_any


def validate_interaction_guild(interaction: Interaction) -> Guild:
    """Validates an interaction.guild object"""
    if interaction.guild is None:
        raise ValueError("Interaction must be in a guild")
    return interaction.guild


def validate_permissions_r(interaction: Interaction) -> bool:
    """
    Validates if the user has rights to a command.
    Returns:
        True if perms Granted False if not granted
    """
    guild = validate_interaction_guild(interaction)
    data = get_guild_data_r(guild.id)
    permissions_config: dict[str, list[int]] = data["config"]["permissions"]

    member = interaction.user
    if isinstance(member, User):
        raise ValueError("Interaction user must be a Member, not a User")

    # Resolve configured roles and members
    p_c_roles: list[Role] = []
    for role_id in permissions_config.get("roles", []):
        role = guild.get_role(role_id)
        if role is None:
            raise ValueError(f"Could not fetch role {role_id}")
        p_c_roles.append(role)

    p_c_members: list[Member] = []
    for member_id in permissions_config.get("members", []):
        m = guild.get_member(member_id)
        if m is None:
            raise ValueError(f"Could not fetch member {member_id}")
        p_c_members.append(m)

    # Owner or explicitly listed member always allowed
    if guild.owner == member or member in p_c_members:
        return True

    # Check if any of the member's roles are in the permitted roles
    for role in member.roles:
        if role in p_c_roles:
            return True

    # If none matched, deny
    return False

def validate_permissions_l(interaction: Interaction) -> bool:
    """
    Validates if the user has rights to a command.
    Returns:
        True if perms Granted False if not granted
    """
    guild = validate_interaction_guild(interaction)
    data = get_guild_data_l(guild.id)
    permissions_config: dict[str, list[int]] = data["config"]["permissions"]

    member = interaction.user
    if isinstance(member, User):
        raise ValueError("Interaction user must be a Member, not a User")

    # Resolve configured roles and members
    p_c_roles: list[Role] = []
    for role_id in permissions_config.get("roles", []):
        role = guild.get_role(role_id)
        if role is None:
            raise ValueError(f"Could not fetch role {role_id}")
        p_c_roles.append(role)

    p_c_members: list[Member] = []
    for member_id in permissions_config.get("members", []):
        m = guild.get_member(member_id)
        if m is None:
            raise ValueError(f"Could not fetch member {member_id}")
        p_c_members.append(m)

    # Owner or explicitly listed member always allowed
    if guild.owner == member or member in p_c_members:
        return True

    # Check if any of the member's roles are in the permitted roles
    for role in member.roles:
        if role in p_c_roles:
            return True

    # If none matched, deny
    return False

def can_access_role(interaction:Interaction, required_role: Role) -> bool:
    """
    Returns True if the member can access maps requiring `required_role`,
    based on the custom hierarchy list (highest first).
    """
    # Find member's highest rank index
    guild=validate_interaction_guild(interaction)
    guild_data = get_guild_data_l(guild.id)
    hierarchy:list[Any] = guild_data["hierarchy"]
    member = interaction.user
    if isinstance(member, User):
        raise ValueError("Cannot be run outside Guild")
    member_index = None
    for i, rid in enumerate(hierarchy):
        role = member.guild.get_role(int(rid))
        if role and role in member.roles:
            member_index = i
            break

    # Find required role's index
    try:
        required_index = hierarchy.index(required_role.id)
    except ValueError:
        return False  # role not in hierarchy

    if member_index is None:
        return False  # member has no rank in hierarchy

    # Rule: can only access roles at or below your rank
    return member_index <= required_index

def has_permissions_mc(member: Member) -> bool:
    """Checks if has permissions"""
    data = load_mc()
    if str(member.id) in data["permissions"].get("users", []):
        return True
    member_roles = [role.name for role in member.roles]
    for role in data["permissions"].get("roles", []):
        if role in member_roles:
            return True
    return False

def check_for_guild_data(file:str, guild:Guild|int):
    """Checks for guild data"""
    if isinstance(guild, Guild):
        guild = guild.id
    data=load_any(file)
    match data[str(guild)]:
        case {"":""}:
            return False
        case None:
            return False
        case _:
            return True