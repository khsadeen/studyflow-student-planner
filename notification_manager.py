from datetime import datetime, timedelta


def get_date_status(date_text):
    try:
        target_date = datetime.strptime(
            date_text,
            "%Y-%m-%d"
        ).date()
    except (TypeError, ValueError):
        return None

    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    if target_date == today:
        return "Today"

    if target_date == tomorrow:
        return "Tomorrow"

    return None


def get_task_alerts(tasks):
    alerts = []

    for task in tasks:
        if task.get("completed", False):
            continue

        due_date = task.get("due_date", "").strip()
        status = get_date_status(due_date)

        if not status:
            continue

        name = task.get("name", "Unnamed task")
        priority = task.get("priority", "Medium")

        alerts.append({
            "kind": "Task",
            "title": name,
            "date": due_date,
            "status": status,
            "priority": priority,
            "message": f"{name} is due {status.lower()}."
        })

    return alerts


def get_event_alerts(events):
    alerts = []

    for event in events:
        date = event.get("date", "").strip()
        status = get_date_status(date)

        if not status:
            continue

        title = event.get("title", "Untitled event")
        event_type = event.get("type", "Other")
        time = event.get("time", "").strip()

        time_text = f" at {time}" if time else ""

        alerts.append({
            "kind": "Event",
            "title": title,
            "date": date,
            "status": status,
            "type": event_type,
            "message": f"{title} is scheduled {status.lower()}{time_text}."
        })

    return alerts


def get_all_alerts(tasks, events):
    alerts = get_task_alerts(tasks)
    alerts.extend(get_event_alerts(events))

    return alerts
