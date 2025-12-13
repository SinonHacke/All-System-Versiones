import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

DATA_FILE = "todo_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"users": {}, "todo": {}}, f, indent=4)
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    if "users" not in data:
        data["users"] = {}
    if "todo" not in data:
        data["todo"] = {}
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class TodoBackend:
    def __init__(self):
        self.data = load_data()

    def get_tasks(self, user):
        return self.data["todo"].get(user, [])

    def add_task(self, user, title):
        self.data["todo"].setdefault(user, [])
        self.data["todo"][user].append({"title": title, "done": False})
        save_data(self.data)

    def toggle_task(self, user, idx):
        self.data["todo"][user][idx]["done"] ^= True
        save_data(self.data)

    def delete_task(self, user, idx):
        self.data["todo"][user].pop(idx)
        save_data(self.data)


class TodoApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("450x550")
        self.window.title("To-Do List")
        self.bg_color = "#d0e7f9" 
        self.window.config(bg=self.bg_color)
        self.backend = TodoBackend()
        self.current_user = None

        self.login_screen()
        self.window.mainloop()

    def clear(self):
        for w in self.window.winfo_children():
            w.destroy()

    def login_screen(self):
        self.clear()
        tk.Label(self.window, text="Username", bg=self.bg_color).pack(pady=5)
        self.u = tk.Entry(self.window)
        self.u.pack(pady=5)

        tk.Label(self.window, text="Password", bg=self.bg_color).pack(pady=5)
        self.p = tk.Entry(self.window, show="*")
        self.p.pack(pady=5)

        tk.Button(self.window, text="Login", width=20, bg="#3f6fb0", fg="white",
                  command=self.login).pack(pady=10)
        tk.Button(self.window, text="Sign Up", width=20, bg="#16a085", fg="white",
                  command=self.signup).pack(pady=5)

    def login(self):
        d = load_data()
        if self.u.get() in d["users"] and d["users"][self.u.get()] == self.p.get():
            self.current_user = self.u.get()
            self.todo_menu()
        else:
            messagebox.showerror("Error", "Wrong login")

    def signup(self):
        d = load_data()
        username = self.u.get().strip()
        password = self.p.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Enter username and password")
            return
        if username in d["users"]:
            messagebox.showerror("Error", "Username exists")
            return
        d["users"][username] = password
        save_data(d)
        messagebox.showinfo("Done", "Account created")

 
    def todo_menu(self):
        self.clear()
        tk.Label(self.window, text=f"To-Do List: {self.current_user}", font=("Arial", 16),
                 bg=self.bg_color).pack(pady=10)

        tk.Button(self.window, text="Add Task", width=25, bg="#3f6fb0", fg="white", command=self.add_task).pack(pady=5)
        tk.Button(self.window, text="List Tasks", width=25, bg="#4caf50", fg="white", command=self.list_tasks).pack(pady=5)
        tk.Button(self.window, text="Mark Done", width=25, bg="#f39c12", fg="white", command=self.mark_done).pack(pady=5)
        tk.Button(self.window, text="Delete Task", width=25, bg="#e74c3c", fg="white", command=self.delete_task).pack(pady=5)
        tk.Button(self.window, text="Logout", width=25, bg="#9b59b6", fg="white", command=self.login_screen).pack(pady=10)

    def add_task(self):
        t = simpledialog.askstring("Task", "Task name")
        if t:
            self.backend.add_task(self.current_user, t)
            messagebox.showinfo("Done", "Task added")

    def list_tasks(self):
        self.clear()
        tk.Label(self.window, text=f"Tasks for {self.current_user}", font=("Arial", 16), bg=self.bg_color).pack(pady=10)
        tasks = self.backend.get_tasks(self.current_user)
        if not tasks:
            tk.Label(self.window, text="No tasks", bg=self.bg_color).pack()
        else:
            tasks_sorted = sorted(tasks, key=lambda x: x["done"])
            for i, t in enumerate(tasks_sorted):
                if t["done"]:
                    bg_color = "#d4edda"  
                    fg_color = "#155724"
                    status = "✔"
                else:
                    bg_color = "#f8d7da"  
                    fg_color = "#721c24"
                    status = "✖"
                tk.Label(self.window, text=f"{i+1}. {t['title']} [{status}]",
                         bg=bg_color, fg=fg_color, anchor="w", width=40, font=("Arial", 12)).pack(padx=10, pady=2)
        tk.Button(self.window, text="Back", width=25, bg="#3f6fb0", fg="white", command=self.todo_menu).pack(pady=10)

    def mark_done(self):
        i = simpledialog.askinteger("Done", "Task number")
        if i is not None:
            tasks = self.backend.get_tasks(self.current_user)
            if 1 <= i <= len(tasks):
                self.backend.toggle_task(self.current_user, i-1)
                messagebox.showinfo("Done", "Task status toggled")
            else:
                messagebox.showerror("Error", "Invalid task number")

    def delete_task(self):
        i = simpledialog.askinteger("Delete", "Task number")
        if i is not None:
            tasks = self.backend.get_tasks(self.current_user)
            if 1 <= i <= len(tasks):
                self.backend.delete_task(self.current_user, i-1)
                messagebox.showinfo("Done", "Task deleted")
            else:
                messagebox.showerror("Error", "Invalid task number")


TodoApp()
