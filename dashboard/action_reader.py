import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ACTION_FILE = os.path.join(
    BASE_DIR,
    "results",
    "live_actions.json"
)


def get_actions():

    try:

        with open(
            ACTION_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {}