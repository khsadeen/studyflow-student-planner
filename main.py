from tkinter import Tk

from data_manager import load_tasks, save_tasks
from ui import StudyFlowApp


# =========================================================
# Data
# =========================================================

tasks = load_tasks()


# =========================================================
# Save Function
# =========================================================

def save_all_tasks():
    try:
        save_tasks(tasks)
    except TypeError:
        save_tasks()


# =========================================================
# Start Application
# =========================================================

root = Tk()

app = StudyFlowApp(
    root,
    tasks,
    save_all_tasks
)

root.mainloop()