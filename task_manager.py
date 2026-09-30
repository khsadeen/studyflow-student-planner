from datetime import datetime


def is_overdue(task):
    """Return True if the task is incomplete and its due date has passed."""

    if task.get("completed", False):
        return False

    due_date = task.get("due_date", "")

    if not due_date:
        return False

    try:
        due = datetime.strptime(
            due_date,
            "%Y-%m-%d"
        ).date()

        return due < datetime.now().date()

    except ValueError:
        return False


def get_task_status(task):
    """Return the current status of a task."""

    if task.get("completed", False):
        return "Completed"

    if is_overdue(task):
        return "Overdue"

    return "Pending"


def validate_task(name, subject, due_date):
    """
    Validate task information.

    Returns:
        (True, "") when valid
        (False, error_message) when invalid
    """

    if not name.strip():
        return False, "Please enter a task name."

    if not subject.strip():
        return False, "Please enter a subject."

    if due_date.strip():
        try:
            datetime.strptime(
                due_date.strip(),
                "%Y-%m-%d"
            )
        except ValueError:
            return False, "Please use the format YYYY-MM-DD."

    return True, ""


def create_task(name, subject, priority, due_date):
    """Create and return a new task dictionary."""

    return {
        "name": name.strip(),
        "subject": subject.strip(),
        "priority": priority,
        "due_date": due_date.strip(),
        "completed": False
    }


def complete_task(tasks, index):
    """Mark a task as completed."""

    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        return True

    return False


def delete_task(tasks, index):
    """Delete a task by index."""

    if 0 <= index < len(tasks):
        tasks.pop(index)
        return True

    return False


def update_task(
    tasks,
    index,
    name,
    subject,
    priority,
    due_date
):
    """Update an existing task."""

    if not 0 <= index < len(tasks):
        return False

    tasks[index]["name"] = name.strip()
    tasks[index]["subject"] = subject.strip()
    tasks[index]["priority"] = priority
    tasks[index]["due_date"] = due_date.strip()

    return True


def filter_tasks(
    tasks,
    search_text="",
    selected_filter="All Tasks"
):
    """Return task indexes matching search and filter criteria."""

    search_text = search_text.strip().lower()

    matching_indexes = []

    for index, task in enumerate(tasks):

        name = task.get("name", "")
        subject = task.get("subject", "")
        priority = task.get("priority", "")
        due_date = task.get("due_date", "")

        combined_text = (
            f"{name} {subject} {priority} {due_date}"
        ).lower()

        if search_text not in combined_text:
            continue

        if selected_filter == "Pending":

            if task.get("completed", False):
                continue

            if is_overdue(task):
                continue

        elif selected_filter == "Completed":

            if not task.get("completed", False):
                continue

        elif selected_filter == "Overdue":

            if not is_overdue(task):
                continue

        elif selected_filter == "High Priority":

            if priority != "High":
                continue

        elif selected_filter == "Medium Priority":

            if priority != "Medium":
                continue

        elif selected_filter == "Low Priority":

            if priority != "Low":
                continue

        matching_indexes.append(index)

    return matching_indexes