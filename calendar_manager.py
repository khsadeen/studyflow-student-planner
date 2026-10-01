import json
import os
from datetime import datetime


CALENDAR_FILE = "studyflow_calendar.json"


def load_events():
    """
    Load calendar events from the local JSON file.
    """

    if not os.path.exists(CALENDAR_FILE):
        return []

    try:
        with open(
            CALENDAR_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, OSError):
        return []


def save_events(events):
    """
    Save calendar events locally.
    """

    with open(
        CALENDAR_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            events,
            file,
            ensure_ascii=False,
            indent=4
        )


def validate_event(title, event_type, date, time=""):
    """
    Validate calendar event information.
    """

    title = title.strip()
    event_type = event_type.strip()
    date = date.strip()
    time = time.strip()

    if not title:
        return False, "Please enter an event title."

    if not event_type:
        return False, "Please select an event type."

    if not date:
        return False, "Please enter a date."

    try:
        datetime.strptime(
            date,
            "%Y-%m-%d"
        )

    except ValueError:
        return False, "Date must use YYYY-MM-DD format."

    if time:

        try:
            datetime.strptime(
                time,
                "%H:%M"
            )

        except ValueError:
            return False, "Time must use HH:MM format."

    return True, ""


def create_event(
    title,
    event_type,
    date,
    time="",
    notes=""
):
    """
    Create a new calendar event.
    """

    return {
        "title": title.strip(),
        "type": event_type.strip(),
        "date": date.strip(),
        "time": time.strip(),
        "notes": notes.strip()
    }


def delete_event(events, index):
    """
    Delete an event by index.
    """

    if index < 0 or index >= len(events):
        return False

    events.pop(index)

    return True


def update_event(
    events,
    index,
    title,
    event_type,
    date,
    time="",
    notes=""
):
    """
    Update an existing calendar event.
    """

    if index < 0 or index >= len(events):
        return False

    events[index] = {
        "title": title.strip(),
        "type": event_type.strip(),
        "date": date.strip(),
        "time": time.strip(),
        "notes": notes.strip()
    }

    return True


def sort_events(events):
    """
    Return events sorted by date and time.
    """

    def sort_key(event):

        date = event.get(
            "date",
            "9999-12-31"
        )

        time = event.get(
            "time",
            "23:59"
        )

        return (
            date,
            time
        )

    return sorted(
        events,
        key=sort_key
    )


def filter_events(
    events,
    search_text="",
    event_type="All"
):
    """
    Return indexes of events matching the filters.
    """

    search_text = search_text.strip().lower()

    matching_indexes = []

    for index, event in enumerate(events):

        title = event.get(
            "title",
            ""
        ).lower()

        event_type_value = event.get(
            "type",
            ""
        )

        notes = event.get(
            "notes",
            ""
        ).lower()

        combined_text = (
            title
            + " "
            + event_type_value.lower()
            + " "
            + notes
        )

        if search_text not in combined_text:
            continue

        if (
            event_type != "All"
            and event_type_value != event_type
        ):
            continue

        matching_indexes.append(index)

    return matching_indexes


def get_events_for_date(
    events,
    date
):
    """
    Return all events for a specific date.
    """

    return [
        event
        for event in events
        if event.get("date") == date
    ]