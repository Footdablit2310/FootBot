import json
import os
from typing import Any, Dict

DATA_FILE: str = "data.json"

def load_all() -> Dict[str, Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf8") as f:
        return json.load(f)

def save_all(data: Dict[str, Dict[str, Any]]) -> None:
    with open(DATA_FILE, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2)

def get_guild_data(guild_id: int) -> Dict[str, Any]:
    all_data: Dict[str, Dict[str, Any]] = load_all()
    gid: str = str(guild_id)
    if gid not in all_data:
        all_data[gid] = {
            "config": {"pingMinutesBefore": 15},
            "rosters": {},
            "events": {}
        }
        save_all(all_data)
    return all_data[gid]

def set_guild_data(guild_id: int, new_data: Dict[str, Any]) -> None:
    all_data: Dict[str, Dict[str, Any]] = load_all()
    all_data[str(guild_id)] = new_data
    save_all(all_data)
