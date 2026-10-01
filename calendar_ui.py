import tkinter as tk
from tkinter import ttk, messagebox

from calendar_manager import (
    load_events,
    save_events,
    validate_event,
    create_event,
    delete_event,
    update_event,
    sort_events,
)


class CalendarApp:
    def __init__(self, root):
        self.root = root

        self.root.title("StudyFlow - Calendar")
        self.root.geometry("1050x650")
        self.root.minsize(900, 550)
        self.root.configure(bg="#F4F6FB")

        # =========================
        # Colors
        # =========================

        self.BG = "#F4F6FB"
        self.WHITE = "#FFFFFF"
        self.DARK = "#202938"
        self.PRIMARY = "#5B5FEF"
        self.PRIMARY_DARK = "#4548C8"
        self.GREEN = "#27AE60"
        self.RED = "#E74C3C"
        self.ORANGE = "#F39C12"
        self.GRAY = "#6B7280"
        self.LIGHT_GRAY = "#E5E7EB"

        # =========================
        # Data
        # =========================

        self.events = load_events()
        self.selected_index = None

        self.build_ui()
        self.refresh_events()

    # =========================
    # Main UI
    # =========================

    def build_ui(self):

        # Header
        header = tk.Frame(
            self.root,
            bg=self.DARK,
            height=80
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="StudyFlow Calendar",
            font=("Arial", 25, "bold"),
            bg=self.DARK,
            fg="white"
        )
        title.pack(
            side="left",
            padx=30,
            pady=18
        )

        subtitle = tk.Label(
            header,
            text="Exams, assignments and important dates",
            font=("Arial", 11),
            bg=self.DARK,
            fg="#B9C0CC"
        )
        subtitle.pack(
            side="left",
            pady=22
        )

        # Content
        content = tk.Frame(
            self.root,
            bg=self.BG
        )
        content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # =========================
        # Left Panel
        # =========================

        left_panel = tk.Frame(
            content,
            bg=self.WHITE,
            width=310,
            highlightbackground=self.LIGHT_GRAY,
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
            text="Add Calendar Event",
            font=("Arial", 18, "bold"),
            bg=self.WHITE,
            fg=self.DARK
        )

        form_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 18)
        )

        # Event title
        tk.Label(
            left_panel,
            text="Event title",
            font=("Arial", 10, "bold"),
            bg=self.WHITE,
            fg=self.DARK
        ).pack(
            anchor="w",
            padx=20
        )

        self.title_entry = tk.Entry(
            left_panel,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.title_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=6
        )

        # Event type
        tk.Label(
            left_panel,
            text="Event type",
            font=("Arial", 10, "bold"),
            bg=self.WHITE,
            fg=self.DARK
        ).pack(
            anchor="w",
            padx=20
        )

        self.type_var = tk.StringVar(
            value="Exam"
        )

        self.type_box = ttk.Combobox(
            left_panel,
            textvariable=self.type_var,
            values=[
                "Exam",
                "Assignment",
                "Lecture",
                "Project",
                "Other"
            ],
            state="readonly",
            font=("Arial", 10)
        )

        self.type_box.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=4
        )

        # Date
        tk.Label(
            left_panel,
            text="Date (YYYY-MM-DD)",
            font=("Arial", 10, "bold"),
            bg=self.WHITE,
            fg=self.DARK
        ).pack(
            anchor="w",
            padx=20
        )

        self.date_entry = tk.Entry(
            left_panel,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.date_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=6
        )

        # Time
        tk.Label(
            left_panel,
            text="Time (HH:MM) - optional",
            font=("Arial", 10, "bold"),
            bg=self.WHITE,
            fg=self.DARK
        ).pack(
            anchor="w",
            padx=20
        )

        self.time_entry = tk.Entry(
            left_panel,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.time_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=6
        )

        # Notes
        tk.Label(
            left_panel,
            text="Notes - optional",
            font=("Arial", 10, "bold"),
            bg=self.WHITE,
            fg=self.DARK
        ).pack(
            anchor="w",
            padx=20
        )

        self.notes_entry = tk.Entry(
            left_panel,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.notes_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 20),
            ipady=6
        )

        # Add button
        self.add_button = tk.Button(
            left_panel,
            text="+  Add Event",
            font=("Arial", 11, "bold"),
            bg=self.PRIMARY,
            fg="white",
            activebackground=self.PRIMARY_DARK,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.add_event
        )

        self.add_button.pack(
            fill="x",
            padx=20,
            pady=(0, 8),
            ipady=9
        )

        # Clear button
        clear_button = tk.Button(
            left_panel,
            text="Clear Form",
            font=("Arial", 10, "bold"),
            bg=self.LIGHT_GRAY,
            fg=self.DARK,
            relief="flat",
            cursor="hand2",
            command=self.clear_form
        )

        clear_button.pack(
            fill="x",
            padx=20,
            ipady=7
        )

        # =========================
        # Right Panel
        # =========================

        right_panel = tk.Frame(
            content,
            bg=self.WHITE,
            highlightbackground=self.LIGHT_GRAY,
            highlightthickness=1
        )

        right_panel.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Top bar
        top_bar = tk.Frame(
            right_panel,
            bg=self.WHITE
        )

        top_bar.pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            top_bar,
            text="My Calendar",
            font=("Arial", 18, "bold"),
            bg=self.WHITE,
            fg=self.DARK
        ).pack(
            side="left"
        )

        # Search
        tk.Label(
            top_bar,
            text="Search:",
            font=("Arial", 10),
            bg=self.WHITE,
            fg=self.GRAY
        ).pack(
            side="right",
            padx=(0, 8)
        )

        self.search_var = tk.StringVar()

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh_events()
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

        # =========================
        # Filter
        # =========================

        filter_frame = tk.Frame(
            right_panel,
            bg=self.WHITE
        )

        filter_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        tk.Label(
            filter_frame,
            text="Filter:",
            font=("Arial", 10),
            bg=self.WHITE,
            fg=self.GRAY
        ).pack(
            side="left"
        )

        self.filter_var = tk.StringVar(
            value="All"
        )

        self.filter_box = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=[
                "All",
                "Exam",
                "Assignment",
                "Lecture",
                "Project",
                "Other"
            ],
            state="readonly",
            width=15
        )

        self.filter_box.pack(
            side="left",
            padx=(8, 0)
        )

        self.filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_events()
        )

        # =========================
        # Table
        # =========================

        table_frame = tk.Frame(
            right_panel,
            bg=self.WHITE
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 10)
        )

        columns = (
            "Title",
            "Type",
            "Date",
            "Time",
            "Notes"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading(
            "Title",
            text="Event"
        )

        self.tree.heading(
            "Type",
            text="Type"
        )

        self.tree.heading(
            "Date",
            text="Date"
        )

        self.tree.heading(
            "Time",
            text="Time"
        )

        self.tree.heading(
            "Notes",
            text="Notes"
        )

        self.tree.column(
            "Title",
            width=180
        )

        self.tree.column(
            "Type",
            width=100
        )

        self.tree.column(
            "Date",
            width=110
        )

        self.tree.column(
            "Time",
            width=80
        )

        self.tree.column(
            "Notes",
            width=180
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

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

        # =========================
        # Buttons
        # =========================

        buttons_frame = tk.Frame(
            right_panel,
            bg=self.WHITE
        )

        buttons_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.edit_button = tk.Button(
            buttons_frame,
            text="✎ Edit Event",
            font=("Arial", 10, "bold"),
            bg=self.PRIMARY,
            fg="white",
            activebackground=self.PRIMARY_DARK,
            relief="flat",
            cursor="hand2",
            command=self.edit_event
        )

        self.edit_button.pack(
            side="left",
            ipadx=10,
            ipady=7,
            padx=(0, 10)
        )

        delete_button = tk.Button(
            buttons_frame,
            text="Delete",
            font=("Arial", 10, "bold"),
            bg=self.RED,
            fg="white",
            activebackground="#C0392B",
            relief="flat",
            cursor="hand2",
            command=self.remove_event
        )

        delete_button.pack(
            side="right",
            ipadx=15,
            ipady=7
        )

    # =========================
    # Form Functions
    # =========================

    def clear_form(self):

        self.title_entry.delete(
            0,
            tk.END
        )

        self.type_var.set(
            "Exam"
        )

        self.date_entry.delete(
            0,
            tk.END
        )

        self.time_entry.delete(
            0,
            tk.END
        )

        self.notes_entry.delete(
            0,
            tk.END
        )

        self.selected_index = None

        self.add_button.config(
            text="+  Add Event",
            command=self.add_event
        )

    def get_form_data(self):

        return (
            self.title_entry.get(),
            self.type_var.get(),
            self.date_entry.get(),
            self.time_entry.get(),
            self.notes_entry.get()
        )

    # =========================
    # Add Event
    # =========================

    def add_event(self):

        title, event_type, date, time, notes = (
            self.get_form_data()
        )

        valid, error = validate_event(
            title,
            event_type,
            date,
            time
        )

        if not valid:
            messagebox.showwarning(
                "Invalid Event",
                error
            )
            return

        event = create_event(
            title,
            event_type,
            date,
            time,
            notes
        )

        self.events.append(event)

        save_events(self.events)

        self.clear_form()
        self.refresh_events()

        messagebox.showinfo(
            "Event Added",
            "The calendar event was added successfully!"
        )

    # =========================
    # Select Event
    # =========================

    def on_select(self, event):

        selected = self.tree.selection()

        if not selected:
            self.selected_index = None
            return

        item_id = selected[0]

        try:
            self.selected_index = int(
                item_id
            )
        except ValueError:
            self.selected_index = None

    # =========================
    # Edit Event
    # =========================

    def edit_event(self):

        if self.selected_index is None:
            messagebox.showwarning(
                "No Selection",
                "Please select an event first."
            )
            return

        event = self.events[
            self.selected_index
        ]

        self.title_entry.delete(
            0,
            tk.END
        )

        self.title_entry.insert(
            0,
            event.get("title", "")
        )

        self.type_var.set(
            event.get(
                "type",
                "Exam"
            )
        )

        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            event.get("date", "")
        )

        self.time_entry.delete(
            0,
            tk.END
        )

        self.time_entry.insert(
            0,
            event.get("time", "")
        )

        self.notes_entry.delete(
            0,
            tk.END
        )

        self.notes_entry.insert(
            0,
            event.get("notes", "")
        )

        self.add_button.config(
            text="✓ Save Changes",
            command=self.save_edit
        )

    # =========================
    # Save Edit
    # =========================

    def save_edit(self):

        if self.selected_index is None:
            return

        title, event_type, date, time, notes = (
            self.get_form_data()
        )

        valid, error = validate_event(
            title,
            event_type,
            date,
            time
        )

        if not valid:
            messagebox.showwarning(
                "Invalid Event",
                error
            )
            return

        success = update_event(
            self.events,
            self.selected_index,
            title,
            event_type,
            date,
            time,
            notes
        )

        if not success:
            messagebox.showerror(
                "Error",
                "Could not update the selected event."
            )
            return

        save_events(
            self.events
        )

        self.clear_form()
        self.refresh_events()

        messagebox.showinfo(
            "Event Updated",
            "The event was updated successfully!"
        )

    # =========================
    # Delete Event
    # =========================

    def remove_event(self):

        if self.selected_index is None:
            messagebox.showwarning(
                "No Selection",
                "Please select an event first."
            )
            return

        answer = messagebox.askyesno(
            "Delete Event",
            "Are you sure you want to delete this event?"
        )

        if not answer:
            return

        success = delete_event(
            self.events,
            self.selected_index
        )

        if success:

            save_events(
                self.events
            )

            self.clear_form()
            self.refresh_events()

    # =========================
    # Refresh Table
    # =========================

    def refresh_events(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = (
            self.search_var.get()
            .strip()
            .lower()
        )

        selected_type = (
            self.filter_var.get()
        )

        sorted_events = sort_events(
            self.events
        )

        for event in sorted_events:

            title = event.get(
                "title",
                ""
            )

            event_type = event.get(
                "type",
                ""
            )

            date = event.get(
                "date",
                ""
            )

            time = event.get(
                "time",
                ""
            )

            notes = event.get(
                "notes",
                ""
            )

            combined_text = (
                title
                + " "
                + event_type
                + " "
                + notes
            ).lower()

            if search_text not in combined_text:
                continue

            if (
                selected_type != "All"
                and event_type != selected_type
            ):
                continue

            original_index = self.events.index(
                event
            )

            self.tree.insert(
                "",
                "end",
                iid=str(original_index),
                values=(
                    title,
                    event_type,
                    date,
                    time,
                    notes
                )
            )


# =========================
# Start Application
# =========================

if __name__ == "__main__":

    root = tk.Tk()

    app = CalendarApp(root)

    root.mainloop()