import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

from gpa_calculator import calculate_gpa


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
        json.dump(
            tasks,
            file,
            ensure_ascii=False,
            indent=4
        )


tasks = load_tasks()


# =========================
# Main Window
# =========================

root = tk.Tk()

root.title("StudyFlow - Student Planner")
root.geometry("1100x720")
root.minsize(950, 650)
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

header = tk.Frame(
    root,
    bg=DARK,
    height=80
)

header.pack(fill="x")
header.pack_propagate(False)


title = tk.Label(
    header,
    text="StudyFlow",
    font=("Arial", 25, "bold"),
    bg=DARK,
    fg="white"
)

title.pack(
    side="left",
    padx=30,
    pady=18
)


subtitle = tk.Label(
    header,
    text="Your personal student planner",
    font=("Arial", 11),
    bg=DARK,
    fg="#B9C0CC"
)

subtitle.pack(
    side="left",
    pady=22
)


# =========================
# Statistics
# =========================

stats_frame = tk.Frame(
    root,
    bg=BG
)

stats_frame.pack(
    fill="x",
    padx=25,
    pady=20
)


def create_stat_card(parent, title_text, value, color):

    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=LIGHT_GRAY,
        highlightthickness=1
    )

    card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=7
    )

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 25, "bold"),
        fg=color,
        bg=WHITE
    )

    value_label.pack(
        pady=(15, 2)
    )

    text_label = tk.Label(
        card,
        text=title_text,
        font=("Arial", 10),
        fg=GRAY,
        bg=WHITE
    )

    text_label.pack(
        pady=(0, 15)
    )

    return value_label


total_value = create_stat_card(
    stats_frame,
    "Total Tasks",
    "0",
    PRIMARY
)

pending_value = create_stat_card(
    stats_frame,
    "Pending",
    "0",
    ORANGE
)

completed_value = create_stat_card(
    stats_frame,
    "Completed",
    "0",
    GREEN
)

overdue_value = create_stat_card(
    stats_frame,
    "Overdue",
    "0",
    RED
)


# =========================
# Content
# =========================

content = tk.Frame(
    root,
    bg=BG
)

content.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(0, 20)
)


# =========================
# Left Panel
# =========================

left_panel = tk.Frame(
    content,
    bg=WHITE,
    width=300,
    highlightbackground=LIGHT_GRAY,
    highlightthickness=1
)

left_panel.pack(
    side="left",
    fill="y",
    padx=(0, 15)
)

left_panel.pack_propagate(False)


form_title = tk.Label(
    left_panel,
    text="Add New Task",
    font=("Arial", 18, "bold"),
    bg=WHITE,
    fg=DARK
)

form_title.pack(
    anchor="w",
    padx=20,
    pady=(20, 15)
)


# =========================
# Task Name
# =========================

tk.Label(
    left_panel,
    text="Task name",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=DARK
).pack(
    anchor="w",
    padx=20
)


task_entry = tk.Entry(
    left_panel,
    font=("Arial", 11),
    relief="solid",
    bd=1
)

task_entry.pack(
    fill="x",
    padx=20,
    pady=(5, 15),
    ipady=6
)


# =========================
# Subject
# =========================

tk.Label(
    left_panel,
    text="Subject",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=DARK
).pack(
    anchor="w",
    padx=20
)


subject_entry = tk.Entry(
    left_panel,
    font=("Arial", 11),
    relief="solid",
    bd=1
)

subject_entry.pack(
    fill="x",
    padx=20,
    pady=(5, 15),
    ipady=6
)


# =========================
# Priority
# =========================

tk.Label(
    left_panel,
    text="Priority",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=DARK
).pack(
    anchor="w",
    padx=20
)


priority_var = tk.StringVar(
    value="Medium"
)


priority_box = ttk.Combobox(
    left_panel,
    textvariable=priority_var,
    values=[
        "Low",
        "Medium",
        "High"
    ],
    state="readonly",
    font=("Arial", 10)
)

priority_box.pack(
    fill="x",
    padx=20,
    pady=(5, 15),
    ipady=4
)


# =========================
# Due Date
# =========================

tk.Label(
    left_panel,
    text="Due date (YYYY-MM-DD)",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=DARK
).pack(
    anchor="w",
    padx=20
)


date_entry = tk.Entry(
    left_panel,
    font=("Arial", 11),
    relief="solid",
    bd=1
)

date_entry.pack(
    fill="x",
    padx=20,
    pady=(5, 20),
    ipady=6
)


# =========================
# Add Task
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
            datetime.strptime(
                due_date,
                "%Y-%m-%d"
            )

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

    task_entry.delete(
        0,
        tk.END
    )

    subject_entry.delete(
        0,
        tk.END
    )

    date_entry.delete(
        0,
        tk.END
    )

    priority_var.set(
        "Medium"
    )

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

add_button.pack(
    fill="x",
    padx=20,
    pady=10,
    ipady=9
)


# =========================
# Right Panel
# =========================

right_panel = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=LIGHT_GRAY,
    highlightthickness=1
)

right_panel.pack(
    side="right",
    fill="both",
    expand=True
)


# =========================
# Search / Filter
# =========================

top_bar = tk.Frame(
    right_panel,
    bg=WHITE
)

top_bar.pack(
    fill="x",
    padx=20,
    pady=20
)


tk.Label(
    top_bar,
    text="My Tasks",
    font=("Arial", 18, "bold"),
    bg=WHITE,
    fg=DARK
).pack(
    side="left"
)


search_var = tk.StringVar()

filter_var = tk.StringVar(
    value="All Tasks"
)


# =========================
# Search
# =========================

search_entry = tk.Entry(
    top_bar,
    textvariable=search_var,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

search_entry.pack(
    side="right",
    ipadx=8,
    ipady=6
)


tk.Label(
    top_bar,
    text="Search:",
    font=("Arial", 10),
    bg=WHITE,
    fg=GRAY
).pack(
    side="right",
    padx=(0, 8)
)


# =========================
# Filter
# =========================

filter_box = ttk.Combobox(
    top_bar,
    textvariable=filter_var,
    values=[
        "All Tasks",
        "Pending",
        "Completed",
        "Overdue",
        "High Priority",
        "Medium Priority",
        "Low Priority"
    ],
    state="readonly",
    font=("Arial", 10),
    width=16
)

filter_box.pack(
    side="right",
    padx=(0, 15),
    ipady=4
)


tk.Label(
    top_bar,
    text="Filter:",
    font=("Arial", 10),
    bg=WHITE,
    fg=GRAY
).pack(
    side="right",
    padx=(0, 8)
)


# =========================
# Task Table
# =========================

table_frame = tk.Frame(
    right_panel,
    bg=WHITE
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 10)
)


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


tree.heading(
    "Task",
    text="Task"
)

tree.heading(
    "Subject",
    text="Subject"
)

tree.heading(
    "Priority",
    text="Priority"
)

tree.heading(
    "Due Date",
    text="Due Date"
)

tree.heading(
    "Status",
    text="Status"
)


tree.column(
    "Task",
    width=180
)

tree.column(
    "Subject",
    width=120
)

tree.column(
    "Priority",
    width=90
)

tree.column(
    "Due Date",
    width=110
)

tree.column(
    "Status",
    width=100
)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)


tree.configure(
    yscrollcommand=scrollbar.set
)


tree.pack(
    side="left",
    fill="both",
    expand=True
)


scrollbar.pack(
    side="right",
    fill="y"
)


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
    selected_filter = filter_var.get()

    for index, task in enumerate(tasks):

        combined_text = (
            task["name"]
            + " "
            + task["subject"]
            + " "
            + task["priority"]
        ).lower()

        # Search
        if search_text not in combined_text:
            continue

        # Filters
        if selected_filter == "Pending":

            if task["completed"] or is_overdue(task):
                continue

        elif selected_filter == "Completed":

            if not task["completed"]:
                continue

        elif selected_filter == "Overdue":

            if not is_overdue(task):
                continue

        elif selected_filter == "High Priority":

            if task["priority"] != "High":
                continue

        elif selected_filter == "Medium Priority":

            if task["priority"] != "Medium":
                continue

        elif selected_filter == "Low Priority":

            if task["priority"] != "Low":
                continue

        # Status
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


# =========================
# Complete Task
# =========================

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


# =========================
# Edit Task
# =========================

def edit_task():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select a task first."
        )

        return

    index = int(selected[0])

    task = tasks[index]


    edit_window = tk.Toplevel(root)

    edit_window.title(
        "Edit Task"
    )

    edit_window.geometry(
        "400x430"
    )

    edit_window.resizable(
        False,
        False
    )

    edit_window.configure(
        bg=WHITE
    )


    tk.Label(
        edit_window,
        text="Edit Task",
        font=("Arial", 20, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(
        pady=(25, 20)
    )


    # Task Name

    tk.Label(
        edit_window,
        text="Task name",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(
        anchor="w",
        padx=35
    )


    edit_name = tk.Entry(
        edit_window,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )

    edit_name.pack(
        fill="x",
        padx=35,
        pady=(5, 15),
        ipady=6
    )

    edit_name.insert(
        0,
        task["name"]
    )


    # Subject

    tk.Label(
        edit_window,
        text="Subject",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(
        anchor="w",
        padx=35
    )


    edit_subject = tk.Entry(
        edit_window,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )

    edit_subject.pack(
        fill="x",
        padx=35,
        pady=(5, 15),
        ipady=6
    )

    edit_subject.insert(
        0,
        task["subject"]
    )


    # Priority

    tk.Label(
        edit_window,
        text="Priority",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(
        anchor="w",
        padx=35
    )


    edit_priority = tk.StringVar(
        value=task["priority"]
    )


    edit_priority_box = ttk.Combobox(
        edit_window,
        textvariable=edit_priority,
        values=[
            "Low",
            "Medium",
            "High"
        ],
        state="readonly",
        font=("Arial", 10)
    )

    edit_priority_box.pack(
        fill="x",
        padx=35,
        pady=(5, 15),
        ipady=4
    )


    # Due Date

    tk.Label(
        edit_window,
        text="Due date (YYYY-MM-DD)",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(
        anchor="w",
        padx=35
    )


    edit_date = tk.Entry(
        edit_window,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )

    edit_date.pack(
        fill="x",
        padx=35,
        pady=(5, 20),
        ipady=6
    )

    edit_date.insert(
        0,
        task["due_date"]
    )


    # Save Edit

    def save_edit():

        name = edit_name.get().strip()
        subject = edit_subject.get().strip()
        priority = edit_priority.get()
        due_date = edit_date.get().strip()


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

                datetime.strptime(
                    due_date,
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Date",
                    "Please use the format YYYY-MM-DD."
                )

                return


        tasks[index]["name"] = name
        tasks[index]["subject"] = subject
        tasks[index]["priority"] = priority
        tasks[index]["due_date"] = due_date

        save_tasks()

        refresh_tasks()

        edit_window.destroy()

        messagebox.showinfo(
            "Task Updated",
            "The task was updated successfully!"
        )


    save_button = tk.Button(
        edit_window,
        text="Save Changes",
        font=("Arial", 11, "bold"),
        bg=PRIMARY,
        fg="white",
        activebackground=PRIMARY_DARK,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=save_edit
    )

    save_button.pack(
        fill="x",
        padx=35,
        pady=10,
        ipady=9
    )


# =========================
# Delete Task
# =========================

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
# GPA Calculator Window
# =========================

def open_gpa_calculator():

    gpa_window = tk.Toplevel(root)

    gpa_window.title(
        "GPA Calculator"
    )

    gpa_window.geometry(
        "680x600"
    )

    gpa_window.resizable(
        False,
        False
    )

    gpa_window.configure(
        bg=BG
    )


    # =========================
    # GPA Header
    # =========================

    tk.Label(
        gpa_window,
        text="GPA Calculator",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=DARK
    ).pack(
        pady=(25, 5)
    )


    tk.Label(
        gpa_window,
        text="Enter your grades and credits",
        font=("Arial", 11),
        bg=BG,
        fg=GRAY
    ).pack(
        pady=(0, 20)
    )


    # =========================
    # GPA Table
    # =========================

    table = tk.Frame(
        gpa_window,
        bg=BG
    )

    table.pack(
        padx=30,
        fill="x"
    )


    tk.Label(
        table,
        text="Subject",
        font=("Arial", 10, "bold"),
        bg=BG,
        fg=DARK
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )


    tk.Label(
        table,
        text="Grade",
        font=("Arial", 10, "bold"),
        bg=BG,
        fg=DARK
    ).grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )


    tk.Label(
        table,
        text="Credits",
        font=("Arial", 10, "bold"),
        bg=BG,
        fg=DARK
    ).grid(
        row=0,
        column=2,
        padx=5,
        pady=5
    )


    subject_entries = []
    grade_entries = []
    credit_entries = []


    for row in range(1, 7):

        subject_entry_gpa = tk.Entry(
            table,
            width=28,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        subject_entry_gpa.grid(
            row=row,
            column=0,
            padx=5,
            pady=6
        )


        grade_entry_gpa = tk.Entry(
            table,
            width=12,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        grade_entry_gpa.grid(
            row=row,
            column=1,
            padx=5,
            pady=6
        )


        credit_entry_gpa = tk.Entry(
            table,
            width=12,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        credit_entry_gpa.grid(
            row=row,
            column=2,
            padx=5,
            pady=6
        )


        subject_entries.append(
            subject_entry_gpa
        )

        grade_entries.append(
            grade_entry_gpa
        )

        credit_entries.append(
            credit_entry_gpa
        )


    # =========================
    # Result
    # =========================

    result_frame = tk.Frame(
        gpa_window,
        bg=WHITE,
        highlightbackground=LIGHT_GRAY,
        highlightthickness=1
    )

    result_frame.pack(
        fill="x",
        padx=30,
        pady=25
    )


    result_label = tk.Label(
        result_frame,
        text="GPA: --",
        font=("Arial", 24, "bold"),
        bg=WHITE,
        fg=PRIMARY
    )

    result_label.pack(
        pady=20
    )


    # =========================
    # Calculate GPA
    # =========================

    def calculate_gpa_from_form():

        courses = []


        for i in range(6):

            subject = subject_entries[i].get().strip()
            grade_text = grade_entries[i].get().strip()
            credit_text = credit_entries[i].get().strip()


            # Empty row
            if not subject and not grade_text and not credit_text:
                continue


            if not grade_text or not credit_text:

                messagebox.showwarning(
                    "Missing Information",
                    "Please enter both grade and credits for every course."
                )

                return


            try:

                grade = float(
                    grade_text
                )

                credits = float(
                    credit_text
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Input",
                    "Grade and credits must be numbers."
                )

                return


            if grade < 0 or grade > 100:

                messagebox.showerror(
                    "Invalid Grade",
                    "Grade must be between 0 and 100."
                )

                return


            if credits <= 0:

                messagebox.showerror(
                    "Invalid Credits",
                    "Credits must be greater than 0."
                )

                return


            courses.append(
                {
                    "grade": grade,
                    "credits": credits
                }
            )


        if not courses:

            messagebox.showwarning(
                "No Courses",
                "Please enter at least one course."
            )

            return


        gpa = calculate_gpa(
            courses
        )


        result_label.config(
            text=f"GPA: {gpa:.2f}"
        )


    calculate_button = tk.Button(
        gpa_window,
        text="Calculate GPA",
        font=("Arial", 11, "bold"),
        bg=PRIMARY,
        fg="white",
        activebackground=PRIMARY_DARK,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=calculate_gpa_from_form
    )

    calculate_button.pack(
        fill="x",
        padx=30,
        ipady=10
    )


# =========================
# Buttons
# =========================

buttons_frame = tk.Frame(
    right_panel,
    bg=WHITE
)

buttons_frame.pack(
    fill="x",
    padx=20,
    pady=15
)


# Edit
edit_button = tk.Button(
    buttons_frame,
    text="✏ Edit Task",
    font=("Arial", 10, "bold"),
    bg=PRIMARY,
    fg="white",
    activebackground=PRIMARY_DARK,
    relief="flat",
    cursor="hand2",
    command=edit_task
)

edit_button.pack(
    side="left",
    ipadx=10,
    ipady=7,
    padx=(0, 10)
)


# Complete
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

complete_button.pack(
    side="left",
    ipadx=10,
    ipady=7
)


# Delete
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

delete_button.pack(
    side="right",
    ipadx=15,
    ipady=7
)


# GPA
gpa_button = tk.Button(
    buttons_frame,
    text="📊 GPA Calculator",
    font=("Arial", 10, "bold"),
    bg=ORANGE,
    fg="white",
    activebackground="#D68910",
    relief="flat",
    cursor="hand2",
    command=open_gpa_calculator
)

gpa_button.pack(
    side="right",
    ipadx=10,
    ipady=7,
    padx=(0, 10)
)


# =========================
# Statistics
# =========================

def update_statistics():

    total = len(tasks)

    completed = sum(
        1
        for task in tasks
        if task["completed"]
    )

    overdue = sum(
        1
        for task in tasks
        if is_overdue(task)
    )

    pending = total - completed - overdue


    total_value.config(
        text=str(total)
    )

    pending_value.config(
        text=str(max(pending, 0))
    )

    completed_value.config(
        text=str(completed)
    )

    overdue_value.config(
        text=str(overdue)
    )


# =========================
# Search / Filter Events
# =========================

search_var.trace_add(
    "write",
    refresh_tasks
)


filter_var.trace_add(
    "write",
    refresh_tasks
)


# =========================
# Keyboard Shortcut
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