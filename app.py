from typing import Any, Optional, Dict
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

from flask import Flask
import vasttrafik
import os
from datetime import datetime
from math import floor

load_dotenv()


def get_next_bus(
    table: Dict[str, Any], line: str, platform: str
) -> Optional[Dict[str, Any]]:
    for bus in table:
        if (
            bus["serviceJourney"]["line"]["name"] == line
            and bus["stopPoint"]["platform"] == platform
        ):
            return bus

    return None


def next_bus_arrival(stop_id: int, line: str, platform: str) -> Optional[int]:
    jp = vasttrafik.JournyPlanner(
        key=os.environ["client_id"],
        secret=os.environ["secret"],
    )

    bus = get_next_bus(jp.arrivalboard(stop_id=stop_id), line, platform)
    if not bus:
        return None

    estimated_arrival = datetime.strptime(
        bus["estimatedTime"][:-7], "%Y-%m-%dT%H:%M:%S.%f"
    )
    return floor((estimated_arrival - datetime.now()).seconds / 60)


app = Flask(__name__)


@app.get("/")
def next_bus() -> str:
    time = next_bus_arrival(9021014014111000, "Buss X4", "B")
    if time is None:
        return "Något gick fel"
    else:
        return f"Bussen kommer om {time} minuter"
