"""The file with Validator Utils"""

from discord import Interaction, Guild, Role, User, Member
from utils.storage import get_guild_data


def validate_interaction_guild(interaction: Interaction) -> Guild:
    """Validates an interaction.guild object"""
    if interaction.guild is None:
        raise ValueError("Guild cannot be None")
    return interaction.guild


def validate_permissions(interaction: Interaction) -> bool:
    """
    Validates if you have rights to a command:
    Returns:
    bool
    """
    guild = validate_interaction_guild(interaction)
    data = get_guild_data(guild.id)
    permissions_config: dict[str, list[int]] = data["config"]["permissions"]
    member = interaction.user
    p_c_members: list[Member] = []
    p_c_roles: list[Role] = []
    p_c_role_ids = permissions_config["roles"]
    p_c_member_ids = permissions_config["members"]
    for p_c_role_id in p_c_role_ids:
        r = guild.get_role(p_c_role_id)
        if r is None:
            raise ValueError("Could not fetch role")
        p_c_roles.append(r)
    for p_c_member_id in p_c_member_ids:
        m = guild.get_member(p_c_member_id)
        if m is None:
            raise ValueError("Could not fetch member")
        p_c_members.append(m)
    if isinstance(member, User):
        raise ValueError("Member/User cannot be a User object")
    member_roles: list[Role] = member.roles
    if guild.owner == member or member in p_c_members:
        return True
    for i in len(member_roles) - 1:  # type: ignore
        if member_roles[i] in p_c_roles:
            return True
        if i == len(member_roles) - 1:
            return False
    raise Exception("Reached unreachable code")
