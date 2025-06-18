import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time

# Main Window
root = tk.Tk()
root.title("To-Do App ")
root.state("zoomed")
root.resizable(True, True)

# List to store tasks: [(title, datetime)]
tasks = []
edit_index = None  # Track index of task being edited

# Background reminder thread
def reminder_checker():
    while True:
        now = datetime.now()
        due_tasks = [tas for tasY in tasks if tas[1] <= now]
        for tas in due_tasks:
            messagebox.showinfo("Task Reminder", f"🕒 Task due: {tas[0]}")
            tasks.remove(tas)
            update_task_list()
        time.sleep(60)

# Add or Save Edit
def add_or_edit_task():
    global edit_index
    title = task_entry.get()
    due_str = due_entry.get()

    if not title or not due_str:
        messagebox.showwarning("Input Error", "Both task and date are required.")
        return

    try:
        due_datetime = datetime.strptime(due_str, "%Y-%m-%d %H:%M")
        if edit_index is not None:
            tasks[edit_index] = (title, due_datetime)
            edit_index = None
            add_button.config(text="Add Task")
        else:
            tasks.append((title, due_datetime))
        update_task_list()
        task_entry.delete(0, tk.END)
        due_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showwarning("Date Format Error", "Use format: YYYY-MM-DD HH:MM")

# Populate fields for editing
def edit_task():
    global edit_index
    selected = listbox.curselection()
    if selected:
        edit_index = selected[0]
        title, due = tasks[edit_index]
        task_entry.delete(0, tk.END)
        task_entry.insert(0, title)
        due_entry.delete(0, tk.END)
        due_entry.insert(0, due.strftime("%Y-%m-%d %H:%M"))
        add_button.config(text="Save Edit")
    else:
        messagebox.showwarning("Selection Error", "Select a task to edit")

def delete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        tasks.pop(index)
        update_task_list()
    else:
        messagebox.showwarning("Selection Error", "Select a task to delete")

def update_task_list():
    listbox.delete(0, tk.END)
    for title, due in tasks:
        listbox.insert(tk.END, f"{title} (Due: {due.strftime('%Y-%m-%d %H:%M')})")

# UI Layout
tk.Label(root, text="🗓️ To-Do List APP", font=("Helvetica", 20, "bold")).pack(pady=10,)

task_entry = tk.Entry(root, font=("Helvetica", 14))
task_entry.pack(pady=5, padx=20, fill=tk.X)
task_entry.insert(0, "Enter task description")

due_entry = tk.Entry(root, font=("Helvetica", 14))
due_entry.pack(pady=5, padx=20, fill=tk.X)
due_entry.insert(0, "Enter due date & time: YYYY-MM-DD HH:MM")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Task", font=("Helvetica", 12), command=add_or_edit_task)
add_button.pack(side=tk.LEFT, padx=10)

edit_button = tk.Button(button_frame, text="Edit Task", font=("Helvetica", 12), command=edit_task)
edit_button.pack(side=tk.LEFT, padx=10)

delete_button = tk.Button(button_frame, text="Delete Task", font=("Helvetica", 12), command=delete_task)
delete_button.pack(side=tk.LEFT, padx=10)

listbox = tk.Listbox(root, font=("Helvetica", 14), height=10, selectbackground="lightblue")
listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Start background reminder thread
threading.Thread(target=reminder_checker, daemon=True).start()

root.mainloop()
