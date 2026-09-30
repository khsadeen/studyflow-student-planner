import tkinter as tk
from tkinter import ttk, messagebox

from gpa_calculator import calculate_gpa
from task_manager import (
    get_task_status,
    validate_task,
    create_task,
    complete_task as manager_complete_task,
    delete_task as manager_delete_task,
    update_task as manager_update_task,
    filter_tasks
)


# =========================================================
# Colors
# =========================================================

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


# =========================================================
# Application
# =========================================================

class StudyFlowApp:

    def __init__(self, root, tasks, save_callback):

        self.root = root
        self.tasks = tasks
        self.save_callback = save_callback

        self.root.title(
            "StudyFlow - Student Planner"
        )

        self.root.geometry(
            "1100x720"
        )

        self.root.minsize(
            950,
            650
        )

        self.root.configure(
            bg=BG
        )

        self.build_interface()

        self.refresh_tasks()


    # =====================================================
    # Main Interface
    # =====================================================

    def build_interface(self):

        self.build_header()

        self.build_statistics()

        content = tk.Frame(
            self.root,
            bg=BG
        )

        content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        self.build_left_panel(content)

        self.build_right_panel(content)

        self.root.bind(
            "<Delete>",
            lambda event: self.delete_task()
        )


    # =====================================================
    # Header
    # =====================================================

    def build_header(self):

        header = tk.Frame(
            self.root,
            bg=DARK,
            height=80
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)


        tk.Label(
            header,
            text="StudyFlow",
            font=("Arial", 25, "bold"),
            bg=DARK,
            fg="white"
        ).pack(
            side="left",
            padx=30,
            pady=18
        )


        tk.Label(
            header,
            text="Your personal student planner",
            font=("Arial", 11),
            bg=DARK,
            fg="#B9C0CC"
        ).pack(
            side="left",
            pady=22
        )


    # =====================================================
    # Statistics
    # =====================================================

    def build_statistics(self):

        stats_frame = tk.Frame(
            self.root,
            bg=BG
        )

        stats_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )


        self.total_value = self.create_stat_card(
            stats_frame,
            "Total Tasks",
            "0",
            PRIMARY
        )

        self.pending_value = self.create_stat_card(
            stats_frame,
            "Pending",
            "0",
            ORANGE
        )

        self.completed_value = self.create_stat_card(
            stats_frame,
            "Completed",
            "0",
            GREEN
        )

        self.overdue_value = self.create_stat_card(
            stats_frame,
            "Overdue",
            "0",
            RED
        )


    def create_stat_card(
        self,
        parent,
        title_text,
        value,
        color
    ):

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


        tk.Label(
            card,
            text=title_text,
            font=("Arial", 10),
            fg=GRAY,
            bg=WHITE
        ).pack(
            pady=(0, 15)
        )


        return value_label


    # =====================================================
    # Left Panel
    # =====================================================

    def build_left_panel(self, parent):

        self.left_panel = tk.Frame(
            parent,
            bg=WHITE,
            width=300,
            highlightbackground=LIGHT_GRAY,
            highlightthickness=1
        )

        self.left_panel.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        self.left_panel.pack_propagate(False)


        tk.Label(
            self.left_panel,
            text="Add New Task",
            font=("Arial", 18, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )


        # Task name

        tk.Label(
            self.left_panel,
            text="Task name",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w",
            padx=20
        )


        self.task_entry = tk.Entry(
            self.left_panel,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.task_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=6
        )


        # Subject

        tk.Label(
            self.left_panel,
            text="Subject",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w",
            padx=20
        )


        self.subject_entry = tk.Entry(
            self.left_panel,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.subject_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=6
        )


        # Priority

        tk.Label(
            self.left_panel,
            text="Priority",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w",
            padx=20
        )


        self.priority_var = tk.StringVar(
            value="Medium"
        )


        self.priority_box = ttk.Combobox(
            self.left_panel,
            textvariable=self.priority_var,
            values=[
                "Low",
                "Medium",
                "High"
            ],
            state="readonly",
            font=("Arial", 10)
        )

        self.priority_box.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=4
        )


        # Due date

        tk.Label(
            self.left_panel,
            text="Due date (YYYY-MM-DD)",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w",
            padx=20
        )


        self.date_entry = tk.Entry(
            self.left_panel,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.date_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 10),
            ipady=6
        )


        # Add button

        tk.Button(
            self.left_panel,
            text="+  Add Task",
            font=("Arial", 11, "bold"),
            bg=PRIMARY,
            fg="white",
            activebackground=PRIMARY_DARK,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.add_task
        ).pack(
            fill="x",
            padx=20,
            pady=10,
            ipady=9
        )


    # =====================================================
    # Right Panel
    # =====================================================

    def build_right_panel(self, parent):

        self.right_panel = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=LIGHT_GRAY,
            highlightthickness=1
        )

        self.right_panel.pack(
            side="right",
            fill="both",
            expand=True
        )


        # Top bar

        top_bar = tk.Frame(
            self.right_panel,
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


        self.search_var = tk.StringVar()

        self.filter_var = tk.StringVar(
            value="All Tasks"
        )


        self.search_entry = tk.Entry(
            top_bar,
            textvariable=self.search_var,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
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


        self.filter_box = ttk.Combobox(
            top_bar,
            textvariable=self.filter_var,
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

        self.filter_box.pack(
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


        # Search events

        self.search_var.trace_add(
            "write",
            self.refresh_tasks
        )

        self.filter_var.trace_add(
            "write",
            self.refresh_tasks
        )


        self.build_task_table()

        self.build_buttons()


    # =====================================================
    # Task Table
    # =====================================================

    def build_task_table(self):

        table_frame = tk.Frame(
            self.right_panel,
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


        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )


        for column in columns:

            self.tree.heading(
                column,
                text=column
            )


        self.tree.column(
            "Task",
            width=180
        )

        self.tree.column(
            "Subject",
            width=120
        )

        self.tree.column(
            "Priority",
            width=90
        )

        self.tree.column(
            "Due Date",
            width=110
        )

        self.tree.column(
            "Status",
            width=100
        )


        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )


        self.tree.configure(
            yscrollcommand=scrollbar.set
        )


        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


    # =====================================================
    # Buttons
    # =====================================================

    def build_buttons(self):

        buttons_frame = tk.Frame(
            self.right_panel,
            bg=WHITE
        )

        buttons_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Button(
            buttons_frame,
            text="✏ Edit Task",
            font=("Arial", 10, "bold"),
            bg=PRIMARY,
            fg="white",
            activebackground=PRIMARY_DARK,
            relief="flat",
            cursor="hand2",
            command=self.edit_task
        ).pack(
            side="left",
            ipadx=10,
            ipady=7,
            padx=(0, 10)
        )


        tk.Button(
            buttons_frame,
            text="✓ Mark as Completed",
            font=("Arial", 10, "bold"),
            bg=GREEN,
            fg="white",
            activebackground="#219150",
            relief="flat",
            cursor="hand2",
            command=self.complete_task
        ).pack(
            side="left",
            ipadx=10,
            ipady=7
        )


        tk.Button(
            buttons_frame,
            text="📊 GPA Calculator",
            font=("Arial", 10, "bold"),
            bg=ORANGE,
            fg="white",
            activebackground="#D68910",
            relief="flat",
            cursor="hand2",
            command=self.open_gpa_calculator
        ).pack(
            side="right",
            ipadx=10,
            ipady=7,
            padx=(0, 10)
        )


        tk.Button(
            buttons_frame,
            text="Delete",
            font=("Arial", 10, "bold"),
            bg=RED,
            fg="white",
            activebackground="#C0392B",
            relief="flat",
            cursor="hand2",
            command=self.delete_task
        ).pack(
            side="right",
            ipadx=15,
            ipady=7
        )


    # =====================================================
    # Refresh Tasks
    # =====================================================

    def refresh_tasks(self, *args):

        if not hasattr(self, "tree"):
            return


        for item in self.tree.get_children():

            self.tree.delete(item)


        indexes = filter_tasks(
            self.tasks,
            self.search_var.get(),
            self.filter_var.get()
        )


        for index in indexes:

            task = self.tasks[index]

            status = get_task_status(task)


            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    task.get("name", ""),
                    task.get("subject", ""),
                    task.get("priority", ""),
                    task.get("due_date", ""),
                    status
                )
            )


        self.update_statistics()


    # =====================================================
    # Statistics
    # =====================================================

    def update_statistics(self):

        total = len(self.tasks)


        completed = sum(
            1
            for task in self.tasks
            if task.get("completed", False)
        )


        overdue = sum(
            1
            for task in self.tasks
            if get_task_status(task) == "Overdue"
        )


        pending = total - completed - overdue


        self.total_value.config(
            text=str(total)
        )

        self.pending_value.config(
            text=str(max(pending, 0))
        )

        self.completed_value.config(
            text=str(completed)
        )

        self.overdue_value.config(
            text=str(overdue)
        )


    # =====================================================
    # Add Task
    # =====================================================

    def add_task(self):

        name = self.task_entry.get()
        subject = self.subject_entry.get()
        priority = self.priority_var.get()
        due_date = self.date_entry.get()


        valid, error_message = validate_task(
            name,
            subject,
            due_date
        )


        if not valid:

            messagebox.showwarning(
                "Invalid Information",
                error_message
            )

            return


        new_task = create_task(
            name,
            subject,
            priority,
            due_date
        )


        self.tasks.append(
            new_task
        )


        self.save_callback()


        self.task_entry.delete(
            0,
            tk.END
        )

        self.subject_entry.delete(
            0,
            tk.END
        )

        self.date_entry.delete(
            0,
            tk.END
        )

        self.priority_var.set(
            "Medium"
        )


        self.refresh_tasks()


        messagebox.showinfo(
            "Task Added",
            "The task was added successfully!"
        )


    # =====================================================
    # Complete Task
    # =====================================================

    def complete_task(self):

        selected = self.tree.selection()


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a task first."
            )

            return


        index = int(
            selected[0]
        )


        success = manager_complete_task(
            self.tasks,
            index
        )


        if success:

            self.save_callback()

            self.refresh_tasks()


    # =====================================================
    # Delete Task
    # =====================================================

    def delete_task(self):

        selected = self.tree.selection()


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a task first."
            )

            return


        index = int(
            selected[0]
        )


        answer = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to delete this task?"
        )


        if not answer:
            return


        success = manager_delete_task(
            self.tasks,
            index
        )


        if success:

            self.save_callback()

            self.refresh_tasks()


    # =====================================================
    # Edit Task
    # =====================================================

    def edit_task(self):

        selected = self.tree.selection()


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a task first."
            )

            return


        index = int(
            selected[0]
        )


        task = self.tasks[index]


        edit_window = tk.Toplevel(
            self.root
        )

        edit_window.title(
            "Edit Task"
        )

        edit_window.geometry(
            "420x470"
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


        # Name

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
            task.get("name", "")
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
            task.get("subject", "")
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
            value=task.get(
                "priority",
                "Medium"
            )
        )


        ttk.Combobox(
            edit_window,
            textvariable=edit_priority,
            values=[
                "Low",
                "Medium",
                "High"
            ],
            state="readonly",
            font=("Arial", 10)
        ).pack(
            fill="x",
            padx=35,
            pady=(5, 15),
            ipady=4
        )


        # Date

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
            task.get("due_date", "")
        )


        def save_edit():

            name = edit_name.get()
            subject = edit_subject.get()
            priority = edit_priority.get()
            due_date = edit_date.get()


            valid, error_message = validate_task(
                name,
                subject,
                due_date
            )


            if not valid:

                messagebox.showwarning(
                    "Invalid Information",
                    error_message
                )

                return


            success = manager_update_task(
                self.tasks,
                index,
                name,
                subject,
                priority,
                due_date
            )


            if success:

                self.save_callback()

                self.refresh_tasks()

                edit_window.destroy()

                messagebox.showinfo(
                    "Task Updated",
                    "The task was updated successfully!"
                )


        tk.Button(
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
        ).pack(
            fill="x",
            padx=35,
            pady=10,
            ipady=9
        )


    # =====================================================
    # GPA Calculator
    # =====================================================

    def open_gpa_calculator(self):

        gpa_window = tk.Toplevel(
            self.root
        )

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


        table = tk.Frame(
            gpa_window,
            bg=BG
        )

        table.pack(
            padx=30,
            fill="x"
        )


        for column, text in enumerate(
            ["Subject", "Grade", "Credits"]
        ):

            tk.Label(
                table,
                text=text,
                font=("Arial", 10, "bold"),
                bg=BG,
                fg=DARK
            ).grid(
                row=0,
                column=column,
                padx=5,
                pady=5
            )


        subject_entries = []
        grade_entries = []
        credit_entries = []


        for row in range(1, 7):

            subject_input = tk.Entry(
                table,
                width=28,
                font=("Arial", 10),
                relief="solid",
                bd=1
            )

            subject_input.grid(
                row=row,
                column=0,
                padx=5,
                pady=6
            )


            grade_input = tk.Entry(
                table,
                width=12,
                font=("Arial", 10),
                relief="solid",
                bd=1
            )

            grade_input.grid(
                row=row,
                column=1,
                padx=5,
                pady=6
            )


            credit_input = tk.Entry(
                table,
                width=12,
                font=("Arial", 10),
                relief="solid",
                bd=1
            )

            credit_input.grid(
                row=row,
                column=2,
                padx=5,
                pady=6
            )


            subject_entries.append(
                subject_input
            )

            grade_entries.append(
                grade_input
            )

            credit_entries.append(
                credit_input
            )


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


        def calculate_gpa_from_form():

            courses = []


            for i in range(6):

                subject = subject_entries[i].get().strip()
                grade_text = grade_entries[i].get().strip()
                credit_text = credit_entries[i].get().strip()


                if not subject and not grade_text and not credit_text:
                    continue


                if not grade_text or not credit_text:

                    messagebox.showwarning(
                        "Missing Information",
                        "Please enter both grade and credits."
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


            try:

                gpa = calculate_gpa(
                    courses
                )

            except Exception as error:

                messagebox.showerror(
                    "GPA Error",
                    str(error)
                )

                return


            result_label.config(
                text=f"GPA: {gpa:.2f}"
            )


        tk.Button(
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
        ).pack(
            fill="x",
            padx=30,
            ipady=10
        )