"""The bot runner"""

import subprocess
import argparse
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# pylint: disable=C0413, E0611

parser = argparse.ArgumentParser()
parser.add_argument(
    "--debug", action="store_true", required=False, help="Use this to enter Debug mode"
)
parser.add_argument(
    "--update-bot",
    action="store_true",
    required=False,
    help="Use this to clear commands for all servers",
)
parser.add_help = True
args = parser.parse_args()

# Resolve paths relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS_PATH = os.path.join(BASE_DIR, "secrets.json")

if __name__ == "__main__":
    BOTS = [
        os.path.join(BASE_DIR, "bot.py"),  # main bot
        os.path.join(BASE_DIR, "roster", "roster_main.py"),
        os.path.join(BASE_DIR, "leaderboard", "leaderboard_main.py"),
    ]

    processes: list[subprocess.Popen[bytes]] = []
    time.sleep(2)
    for bot_path in BOTS:
        print(f"Starting {bot_path}...")
        p = subprocess.Popen(["python", bot_path])
        time.sleep(8)  # Added to block JSON corruption
        processes.append(p)
    time.sleep(8)
    if args.update_bot:
        time.sleep(2)
        print("Stopping all bots...")
        for p in processes:
            p.terminate()
    else:
        try:
            for p in processes:
                p.wait()

        except KeyboardInterrupt:
            print("Stopping all bots...")
            for p in processes:
                p.terminate()
