import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


# =========================
# Data Management
# =========================

DATA_FILE = "studyflow_data.json"


def load_tasks():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []
    return []


def save_tasks():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


tasks = load_tasks()


# =========================
# Main Window
# =========================

root = tk.Tk()
root.title("StudyFlow - Student Planner")
root.geometry("1050x680")
root.minsize(900, 600)
root.configure(bg="#F4F6FB")


# =========================
# Colors
# =========================

BG = "#F4F6FB"
WHITE = "#FFFFFF"
DARK = "#202938"
PRIMARY = "#5B5FEF"
PRIMARY_DARK = "#4548C8"
GREEN = "#27AE60"
RED = "#E74C3C"
ORANGE = "#F39C12"
GRAY = "#6B7280"
LIGHT_GRAY = "#E5E7EB"


# =========================
# Header
# =========================

header = tk.Frame(root, bg=DARK, height=80)
header.pack(fill="x")
header.pack_propagate(False)

title = tk.Label(
    header,
    text="StudyFlow",
    font=("Arial", 25, "bold"),
    bg=DARK,
    fg="white"
)
title.pack(side="left", padx=30, pady=18)

subtitle = tk.Label(
    header,
    text="Your personal student planner",
    font=("Arial", 11),
    bg=DARK,
    fg="#B9C0CC"
)
subtitle.pack(side="left", pady=22)


# =========================
# Statistics
# =========================

stats_frame = tk.Frame(root, bg=BG)
stats_frame.pack(fill="x", padx=25, pady=20)


def create_stat_card(parent, title_text, value, color):
    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=LIGHT_GRAY,
        highlightthickness=1
    )
    card.pack(side="left", expand=True, fill="both", padx=7)

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 25, "bold"),
        fg=color,
        bg=WHITE
    )
    value_label.pack(pady=(15, 2))

    text_label = tk.Label(
        card,
        text=title_text,
        font=("Arial", 10),
        fg=GRAY,
        bg=WHITE
    )
    text_label.pack(pady=(0, 15))

    return value_label


total_value = create_stat_card(
    stats_frame, "Total Tasks", "0", PRIMARY
)

pending_value = create_stat_card(
    stats_frame, "Pending", "0", ORANGE
)

completed_value = create_stat_card(
    stats_frame, "Completed", "0", GREEN
)

overdue_value = create_stat_card(
    stats_frame, "Overdue", "0", RED
)


# =========================
# Content
# =========================

content = tk.Frame(root, bg=BG)
content.pack(fill="both", expand=True, padx=25, pady=(0, 20))


# =========================
# Left Panel - Add Task
# =========================

left_panel = tk.Frame(
    content,
    bg=WHITE,
    width=300,
    highlightbackground=LIGHT_GRAY,
    highlightthickness=1
)
left_panel.pack(side="left", fill="y", padx=(0, 15))
left_panel.pack_propagate(False)

form_title = tk.Label(
    left_panel,
    text="Add New Task",
    font=("Arial", 18, "bold"),
    bg=WHITE,
    fg=DARK
)
form_title.pack(anchor="w", padx=20, pady=(20, 15))


# Task name
tk.Label(
    left_panel,
    text="Task name",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=20)

task_entry = tk.Entry(
    left_panel,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
task_entry.pack(fill="x", padx=20, pady=(5, 15), ipady=6)


# Subject
tk.Label(
    left_panel,
    text="Subject",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=20)

subject_entry = tk.Entry(
    left_panel,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
subject_entry.pack(fill="x", padx=20, pady=(5, 15), ipady=6)


# Priority
tk.Label(
    left_panel,
    text="Priority",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=20)

priority_var = tk.StringVar(value="Medium")

priority_box = ttk.Combobox(
    left_panel,
    textvariable=priority_var,
    values=["Low", "Medium", "High"],
    state="readonly",
    font=("Arial", 10)
)
priority_box.pack(fill="x", padx=20, pady=(5, 15), ipady=4)


# Due date
tk.Label(
    left_panel,
    text="Due date (YYYY-MM-DD)",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=20)

date_entry = tk.Entry(
    left_panel,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
date_entry.pack(fill="x", padx=20, pady=(5, 20), ipady=6)


# =========================
# Add Task Function
# =========================

def add_task():
    name = task_entry.get().strip()
    subject = subject_entry.get().strip()
    priority = priority_var.get()
    due_date = date_entry.get().strip()

    if not name:
        messagebox.showwarning(
            "Missing Information",
            "Please enter a task name."
        )
        return

    if not subject:
        messagebox.showwarning(
            "Missing Information",
            "Please enter a subject."
        )
        return

    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please use the format YYYY-MM-DD."
            )
            return

    new_task = {
        "name": name,
        "subject": subject,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }

    tasks.append(new_task)
    save_tasks()

    task_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    priority_var.set("Medium")

    refresh_tasks()

    messagebox.showinfo(
        "Task Added",
        "The task was added successfully!"
    )


add_button = tk.Button(
    left_panel,
    text="+  Add Task",
    font=("Arial", 11, "bold"),
    bg=PRIMARY,
    fg="white",
    activebackground=PRIMARY_DARK,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=add_task
)
add_button.pack(fill="x", padx=20, pady=10, ipady=9)


# =========================
# Right Panel
# =========================

right_panel = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=LIGHT_GRAY,
    highlightthickness=1
)
right_panel.pack(side="right", fill="both", expand=True)


# =========================
# Search / Filter
# =========================

top_bar = tk.Frame(right_panel, bg=WHITE)
top_bar.pack(fill="x", padx=20, pady=20)

tk.Label(
    top_bar,
    text="My Tasks",
    font=("Arial", 18, "bold"),
    bg=WHITE,
    fg=DARK
).pack(side="left")

search_var = tk.StringVar()

search_entry = tk.Entry(
    top_bar,
    textvariable=search_var,
    font=("Arial", 10),
    relief="solid",
    bd=1
)
search_entry.pack(side="right", ipadx=8, ipady=6)

tk.Label(
    top_bar,
    text="Search:",
    font=("Arial", 10),
    bg=WHITE,
    fg=GRAY
).pack(side="right", padx=(0, 8))


# =========================
# Treeview
# =========================

table_frame = tk.Frame(right_panel, bg=WHITE)
table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

columns = (
    "Task",
    "Subject",
    "Priority",
    "Due Date",
    "Status"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

tree.heading("Task", text="Task")
tree.heading("Subject", text="Subject")
tree.heading("Priority", text="Priority")
tree.heading("Due Date", text="Due Date")
tree.heading("Status", text="Status")

tree.column("Task", width=180)
tree.column("Subject", width=120)
tree.column("Priority", width=90)
tree.column("Due Date", width=110)
tree.column("Status", width=100)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# =========================
# Task Functions
# =========================

def is_overdue(task):
    if task["completed"]:
        return False

    if not task["due_date"]:
        return False

    try:
        due = datetime.strptime(
            task["due_date"],
            "%Y-%m-%d"
        ).date()

        return due < datetime.now().date()

    except:
        return False


def refresh_tasks(*args):
    for item in tree.get_children():
        tree.delete(item)

    search_text = search_var.get().lower()

    for index, task in enumerate(tasks):

        combined_text = (
            task["name"] + " " +
            task["subject"] + " " +
            task["priority"]
        ).lower()

        if search_text not in combined_text:
            continue

        if task["completed"]:
            status = "Completed"
        elif is_overdue(task):
            status = "Overdue"
        else:
            status = "Pending"

        tree.insert(
            "",
            "end",
            iid=str(index),
            values=(
                task["name"],
                task["subject"],
                task["priority"],
                task["due_date"],
                status
            )
        )

    update_statistics()


def complete_task():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a task first."
        )
        return

    index = int(selected[0])

    tasks[index]["completed"] = True

    save_tasks()
    refresh_tasks()


def delete_task():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a task first."
        )
        return

    index = int(selected[0])

    answer = messagebox.askyesno(
        "Delete Task",
        "Are you sure you want to delete this task?"
    )

    if answer:
        tasks.pop(index)
        save_tasks()
        refresh_tasks()


# =========================
# Buttons
# =========================

buttons_frame = tk.Frame(
    right_panel,
    bg=WHITE
)
buttons_frame.pack(fill="x", padx=20, pady=15)

complete_button = tk.Button(
    buttons_frame,
    text="✓ Mark as Completed",
    font=("Arial", 10, "bold"),
    bg=GREEN,
    fg="white",
    activebackground="#219150",
    relief="flat",
    cursor="hand2",
    command=complete_task
)
complete_button.pack(side="left", ipadx=10, ipady=7)

delete_button = tk.Button(
    buttons_frame,
    text="Delete",
    font=("Arial", 10, "bold"),
    bg=RED,
    fg="white",
    activebackground="#C0392B",
    relief="flat",
    cursor="hand2",
    command=delete_task
)
delete_button.pack(side="right", ipadx=15, ipady=7)


# =========================
# Statistics
# =========================

def update_statistics():
    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["completed"]
    )

    overdue = sum(
        1 for task in tasks
        if is_overdue(task)
    )

    pending = total - completed - overdue

    total_value.config(text=str(total))
    pending_value.config(text=str(max(pending, 0)))
    completed_value.config(text=str(completed))
    overdue_value.config(text=str(overdue))


# =========================
# Search Event
# =========================

search_var.trace_add(
    "write",
    refresh_tasks
)


# =========================
# Keyboard Shortcuts
# =========================

root.bind(
    "<Delete>",
    lambda event: delete_task()
)


# =========================
# Initial Load
# =========================

refresh_tasks()


# =========================
# Start Application
# =========================

root.mainloop()