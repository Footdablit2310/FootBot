"""The file with Validator Utils"""

from discord import Interaction, Guild


def validate_interaction_guild(interaction: Interaction) -> Guild:
    """Validates an interaction.guild object"""
    if interaction.guild is None:
        raise ValueError("Guild cannot be None")
    return interaction.guild
