import json
from pathlib import Path

try:
    with open("app/data/bites.json") as f:
        BITES = json.load(f)
        if not isinstance(BITES, dict):
            raise ValueError("JSON content is not a dictionary.")
except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
    BITES = {}
    print(f"Error loading bites.json: {e}")

def get_bite(feature: str) -> str:
    print(f"Available keys: {list(BITES.keys())}")
    print(f"Feature: {feature}")
    print(f"Debugy: {BITES.get(feature)}")
    return BITES.get(feature, "No Jargon bite found")