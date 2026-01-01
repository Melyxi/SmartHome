from pathlib import Path

default_setting = {"city": "Москва", "refresh_time": 30, "temperature_display_mode": "celsius", "last_update": None}
JSON_FILE_PATH = Path(__file__).parent / "weather.json"
UUID_FILE_PATH = Path(__file__).parent / ".uuid"
EXPOSES_PATH = Path(__file__).parent / "exposes.json"
