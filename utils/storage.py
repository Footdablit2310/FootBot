"""Handles all read and write operations"""

from logging import Logger
import json
import os
from typing import Any, Dict

ROSTER_DATA_FILE: str = "roster_data.json"


def load_all_r() -> Dict[str, Dict[str, Any]]:
    """Loads ALL the data in roster_data.json"""
    if not os.path.exists(ROSTER_DATA_FILE):
        return {}
    with open(ROSTER_DATA_FILE, "r", encoding="utf8") as f:
        return json.load(f)


def save_all_r(data: Dict[str, Dict[str, Any]]) -> None:
    """Saves ALL the data in roster_data.json"""
    with open(ROSTER_DATA_FILE, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)


def get_guild_data_r(guild_id: int) -> Dict[str, Any]:
    """Gets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_all_r()
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
        save_all_r(all_data)
    return all_data[gid]


def set_guild_data_r(guild_id: int, new_data: Dict[str, Any]) -> None:
    """Sets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_all_r()
    all_data[str(guild_id)] = new_data
    save_all_r(all_data)


LEADERBOARD_DATA_FILE: str = "leaderboard_data.json"


def load_all_l() -> Dict[str, Dict[str, Any]]:
    """Loads ALL the data in leaderboard_data.json"""
    if not os.path.exists(LEADERBOARD_DATA_FILE):
        return {}
    with open(LEADERBOARD_DATA_FILE, "r", encoding="utf8") as f:
        return json.load(f)


def save_all_l(data: Dict[str, Dict[str, Any]]) -> None:
    """Saves ALL the data in leaderboard_data.json"""
    with open(LEADERBOARD_DATA_FILE, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)


def get_guild_data_l(guild_id: int) -> Dict[str, Any]:
    """Gets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_all_l()
    gid: str = str(guild_id)
    if gid not in all_data:
        all_data[gid] = {
            "config": {"permissions": {"roles": [], "members": []}},
            "maps": [],
            "leaderboard": [],
            "hierarchy": [],
        }
        save_all_l(all_data)
    return all_data[gid]


def set_guild_data_l(guild_id: int, new_data: Dict[str, Any]) -> None:
    """Sets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_all_l()
    all_data[str(guild_id)] = new_data
    save_all_l(all_data)


CMD_LST_FILE = "command_list.json"


def command_list_add(string: str):
    """CLA"""
    json_data: dict[str, list[str]] = {"": [""]}
    if not os.path.exists(CMD_LST_FILE):
        json_data = {"": [""]}
    with open(CMD_LST_FILE, "r", encoding="utf8") as f:
        json_data = json.load(f)
    commands = json_data["cmds"]
    commands.append(string)
    json_data["cmds"] = commands
    with open(CMD_LST_FILE, "w", encoding="utf8") as f:
        json.dump(json_data, f, indent=4)


def print_command_list(log: Logger):
    """PCL"""
    json_data: dict[str, list[str]] = {"": [""]}
    if not os.path.exists(CMD_LST_FILE):
        json_data = {"": [""]}
    with open(CMD_LST_FILE, "r", encoding="utf8") as f:
        json_data = json.load(f)
    command_names = json_data["cmds"]
    for command_name in command_names:
        log.debug("Command: /%s has been loaded", command_name)

MC_FILE = "mc.json"

def load_mc() -> Dict[str, Any]:
    """Saves data for the minecraft system"""
    try:
        with open(MC_FILE, "r", encoding="utf-8") as f:
            json_data:Dict[str, Any] = json.load(f)
        return json_data
    except FileNotFoundError as FNFE:
        raise ValueError from FNFE


def save_mc(data: Dict[str, Any]) -> None:
    """Saves data for the minecraft system"""
    with open(MC_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_guild_data_mc(guild_id: int) -> Dict[str, Any]:
    """Handles fetching guild data for a Minecraft type"""
    data = load_mc()
    return data["guilds"].setdefault(
        str(guild_id),
        {
            "rcon": {"host": "", "port": 25575, "password": ""},
            "links": {},
            "permissions": {"users": [], "roles": []}
        }
    )

def load_any(file:str) -> Dict[str, Any|None]:
    """Saves data for the minecraft system"""
    try:
        with open(file, "r", encoding="utf-8") as f:
            json_data:Dict[str, Any|None] = json.load(f)
        return json_data
    except FileNotFoundError as FNFE:
        raise ValueError from FNFE

def save_any(file:str, data: Dict[str, Any]) -> None:
    """Saves data for the minecraft system"""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
