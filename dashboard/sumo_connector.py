import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

METRICS_FILE = os.path.join(
    BASE_DIR,
    "results",
    "live_metrics.json"
)

TLS_IDS = [
    "A0", "A1", "A2",
    "B0", "B1", "B2",
    "C0", "C1", "C2"
]


def get_default_data():

    return {
        tls: {
            "queue": 0,
            "wait": 0,
            "phase": "UNKNOWN"
        }
        for tls in TLS_IDS
    }


def get_agent_data():

    try:

        if not os.path.exists(METRICS_FILE):
            print("File not found:", METRICS_FILE)
            return get_default_data()

        with open(
            METRICS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return data

    except Exception as e:

        print("Dashboard read error:", e)

        return get_default_data()