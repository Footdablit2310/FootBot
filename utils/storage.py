"""Handles all read and write operations"""

from enum import Enum
from logging import Logger
import json
import os
from typing import Any, Dict


class DataFiles(Enum):
    """All the data Files used in one centralized Enum"""

    ROSTER_DATA_FILE = "roster_data.json"
    LEADERBOARD_DATA_FILE = "leaderboard_data.json"
    CMD_LST_FILE = ".json"
    MCLINK_DATA_FILE = "mcdata.json"


ROSTER_DATA_FILE = DataFiles.ROSTER_DATA_FILE
LEADERBOARD_DATA_FILE = DataFiles.LEADERBOARD_DATA_FILE
CMD_LST_FILE = DataFiles.CMD_LST_FILE
MCLINK_DATA_FILE = DataFiles.MCLINK_DATA_FILE


class SubDivsions(Enum):
    """The enum to handle subdivisions"""

    LEADERBOARD = "Leaderboard"
    ROSTER = "Roster"
    MAIN = "Main"
    MCLINK = "MCLink"


LEADERBOARD = SubDivsions.LEADERBOARD
ROSTER = SubDivsions.ROSTER
MAIN = SubDivsions.MAIN
MCLINK = SubDivsions.MCLINK


def load_json_file(file_path: str | DataFiles, default: Any = None) -> Any:
    """Loads JSON data from a file, returning a default value when missing."""
    if isinstance(file_path, DataFiles):
        file_path = file_path.value
    if not os.path.exists(file_path):
        return default
    with open(file_path, "r", encoding="utf8") as f:
        return json.load(f)


def save_json_file(file_path: str | DataFiles, data: Any) -> None:
    """Saves JSON data to a file."""
    if isinstance(file_path, DataFiles):
        file_path = file_path.value
    with open(file_path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)


def get_guild_data_r(guild_id: int) -> Dict[str, Any]:
    """Gets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_json_file(ROSTER_DATA_FILE)
    gid: str = str(guild_id)
    if gid not in all_data:
        all_data[gid] = {
            "config": {
                "pingMinutesBefore": 15,
                "permissions": {"roles": [], "members": []},
            },
            "rosters": {},
            "events": {},
        }
        save_json_file(ROSTER_DATA_FILE, all_data)
    return all_data[gid]


def set_guild_data_r(guild_id: int, new_data: Dict[str, Any]) -> None:
    """Sets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_json_file(ROSTER_DATA_FILE)
    all_data[str(guild_id)] = new_data
    save_json_file(ROSTER_DATA_FILE, all_data)


def get_guild_data_l(guild_id: int) -> Dict[str, Any]:
    """Gets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_json_file(LEADERBOARD_DATA_FILE)
    gid: str = str(guild_id)
    if gid not in all_data:
        all_data[gid] = {
            "config": {"permissions": {"roles": [], "members": []}},
            "maps": [],
            "leaderboard": [],
            "hierarchy": [],
        }
        save_json_file(LEADERBOARD_DATA_FILE, all_data)
    return all_data[gid]


def set_guild_data_l(guild_id: int, new_data: Dict[str, Any]) -> None:
    """Sets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_json_file(LEADERBOARD_DATA_FILE)
    all_data[str(guild_id)] = new_data
    save_json_file(LEADERBOARD_DATA_FILE, all_data)

def print_(log: Logger):
    """PCL"""
    json_data: dict[str, list[str]] = load_json_file(CMD_LST_FILE, {"cmds": []})
    command_names = json_data.get("cmds", [])
    for command_name in command_names:
        log.debug(
            'Command: /%s from SubDivision: "%s" has been loaded',
            command_name.split("|", 2)[0],
            command_name.split("|", 2)[1],
        )
