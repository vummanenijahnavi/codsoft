import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

class TaskManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def add_task(self, description):
        self.tasks.append({"description": description, "completed": False})
        self.save_tasks()

    def edit_task(self, index, new_description):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["description"] = new_description
            self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()

    def save_tasks(self):
        with open(self.file_path, "w") as file:
            json.dump(self.tasks, file, indent=2)

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        else:
            return []

class TodoApp(tk.Tk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.title("To-Do List Application")
        self.geometry("400x400")

        # Configure colors
        self.configure(bg="#ffe4e1")  # Background color: Dark Blue
        self.label_color = "#FFFFFF"  # Text color: White
        self.button_color = "#008000" # Button color: Green
        self.entry_text_color = "#000000" # Text color for entry widget: Black

        self.subheading_label = tk.Label(self, text="Enter Task to Add:", bg="#ffe4e1", fg="#008000")
        self.subheading_label.pack(pady=(10, 5))
        
        # Entry box for adding new tasks
        self.task_entry = tk.Entry(self, bg="#FFFFFF", fg=self.entry_text_color)
        self.task_entry.pack(fill=tk.X, padx=10, pady=10)

        # Button to submit a new task
        submit_button = tk.Button(self, text="Add Task", bg=self.button_color, fg="#FFFFFF", command=self.add_task)
        submit_button.pack(padx=10, pady=10)

        self.subheading_label = tk.Label(self, text="Tasks To Do:", bg="#ffe4e1", fg="#008000")
        self.subheading_label.pack(pady=(10, 5))
        
        # Listbox to display tasks
        self.task_list = tk.Listbox(self, selectmode=tk.SINGLE, bg="#FFFFFF", fg=self.label_color)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame for action buttons
        action_frame = tk.Frame(self, bg="#ffe4e1")
        action_frame.pack(fill=tk.X)

        # Button to edit a task
        edit_button = tk.Button(action_frame, text="Edit Task", bg=self.button_color, fg="#FFFFFF", command=self.edit_task)
        edit_button.pack(side=tk.LEFT, padx=10)

        # Button to delete a task
        delete_button = tk.Button(action_frame, text="Delete Task", bg=self.button_color, fg="#FFFFFF", command=self.delete_task)
        delete_button.pack(side=tk.RIGHT, padx=10)

        self.update_task_list()

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for i, task in enumerate(self.task_manager.tasks):
            self.task_list.insert(tk.END, f"{i + 1}. {task['description']}")

    def add_task(self):
        task_description = self.task_entry.get()
        if task_description:
            self.task_manager.add_task(task_description)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Task description cannot be empty.")

    def edit_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            # Use a simple dialog to get the new description
            new_description = simpledialog.askstring("Edit Task", "Enter new description:")
            if new_description:
                self.task_manager.edit_task(selected_index[0], new_description)
                self.update_task_list()
        else:
            messagebox.showerror("Error", "Select a task to edit.")

    def delete_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            self.task_manager.delete_task(selected_index[0])
            self.update_task_list()
        else:
            messagebox.showerror("Error", "Select a task to delete.")

def main():
    task_manager = TaskManager("tasks.json")
    app = TodoApp(task_manager)
    app.mainloop()

if __name__ == "__main__":
    main()
