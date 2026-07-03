"""The file with Validator Utils"""

from discord import Interaction, Guild, Role, User, Member
from utils.storage import get_guild_data_r, get_guild_data_l


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
