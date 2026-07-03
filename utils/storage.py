"""Handles all read and write operations"""

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
        json.dump(data, f, indent=2)


def get_guild_data_r(guild_id: int) -> Dict[str, Any]:
    """Gets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_all_r()
    gid: str = str(guild_id)
    if gid not in all_data:
        all_data[gid] = {
            "config": {
                "pingMinutesBefore": 15,
                "permissions": {
                    "roles":[],
                    "members":[]
                }
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
        json.dump(data, f, indent=2)


def get_guild_data_l(guild_id: int) -> Dict[str, Any]:
    """Gets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_all_l()
    gid: str = str(guild_id)
    if gid not in all_data:
        all_data[gid] = {
            "config": {
                "permissions": {
                    "roles":[],
                    "members":[]
                }
            },
            "maps": [],
            "leaderboard": [],
        }
        save_all_l(all_data)
    return all_data[gid]


def set_guild_data_l(guild_id: int, new_data: Dict[str, Any]) -> None:
    """Sets the guild specific data"""
    all_data: Dict[str, Dict[str, Any]] = load_all_l()
    all_data[str(guild_id)] = new_data
    save_all_l(all_data)
