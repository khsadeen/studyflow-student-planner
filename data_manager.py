import json
import os


DATA_FILE = "studyflow_data.json"


def load_tasks():
    """Load saved tasks from the JSON file."""

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            tasks,
            file,
            ensure_ascii=False,
            indent=4
        )