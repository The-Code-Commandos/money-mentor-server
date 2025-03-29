import json
from pathlib import Path

# load the JSON file
data_file = Path(__file__).parent.parent / "data" / "bites.json"

try:
    with data_file.open() as f:
        BITES = json.load(f)
        if not isinstance(BITES, dict):
            raise ValueError("JSON content is not a dictionary.")
except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
    BITES = {}
    print(f"Error loading bites.json: {e}")

def get_bite(feature: str) -> str:
    return BITES.get(feature, "No Jargon bite found")