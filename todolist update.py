import tkinter as tk
from tkinter import messagebox, simpledialog
from todo_backend import TodoListBackend

class TodoApp_Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("450x550")
        self.window.title("To-Do List")
        self.bg_color = "#d0e7f9"
        self.window.config(bg=self.bg_color)

        self.backend = TodoListBackend()
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

        tk.Button(
            self.window, text="Login", width=20,
            bg="#3f6fb0", fg="white",
            command=self.handle_login
        ).pack(pady=10)

        tk.Button(
            self.window, text="Sign Up", width=20,
            bg="#16a085", fg="white",
            command=self.handle_signup
        ).pack(pady=5)

    def handle_login(self):
        username = self.u.get().strip()
        password = self.p.get().strip()
        if self.backend.validate_login(username, password):
            self.current_user = username
            self.todo_menu()
        else:
            messagebox.showerror("Error", "Wrong login")

    def handle_signup(self):
        username = self.u.get().strip()
        password = self.p.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "Enter username and password")
            return

        ok = self.backend.create_user(username, password)
        if ok:
            messagebox.showinfo("Done", "Account created")
        else:
            messagebox.showerror("Error", "Username exists")

    def todo_menu(self):
        self.clear()

        tk.Label(
            self.window,
            text=f"To-Do List: {self.current_user}",
            font=("Arial", 16),
            bg=self.bg_color
        ).pack(pady=10)

        tk.Button(self.window, text="Add Task", width=25,
                  bg="#3f6fb0", fg="white",
                  command=self.add_task).pack(pady=5)

        tk.Button(self.window, text="List Tasks", width=25,
                  bg="#4caf50", fg="white",
                  command=self.list_tasks).pack(pady=5)

        tk.Button(self.window, text="Mark Done", width=25,
                  bg="#f39c12", fg="white",
                  command=self.mark_done).pack(pady=5)

        tk.Button(self.window, text="Delete Task", width=25,
                  bg="#e74c3c", fg="white",
                  command=self.delete_task).pack(pady=5)

        tk.Button(self.window, text="Logout", width=25,
                  bg="#9b59b6", fg="white",
                  command=self.login_screen).pack(pady=10)

    def add_task(self):
        t = simpledialog.askstring("Task", "Task name")
        if t:
            self.backend.add_task(self.current_user, t)
            messagebox.showinfo("Done", "Task added")

    def list_tasks(self):
        self.clear()

        tk.Label(
            self.window,
            text=f"Tasks for {self.current_user}",
            font=("Arial", 16),
            bg=self.bg_color
        ).pack(pady=10)

        tasks = self.backend.get_tasks(self.current_user)

        if not tasks:
            tk.Label(self.window, text="No tasks", bg=self.bg_color).pack()
        else:
            for i, t in enumerate(tasks):
                if t["done"]:
                    bg_color = "#d4edda"
                    fg_color = "#155724"
                    status = "done"
                else:
                    bg_color = "#f8d7da"
                    fg_color = "#721c24"
                    status = "under work"

                tk.Label(
                    self.window,
                    text=f"{i+1}. {t['title']} [{status}]",
                    bg=bg_color, fg=fg_color,
                    width=40, anchor="w",
                    font=("Arial", 12)
                ).pack(padx=10, pady=2)

        tk.Button(
            self.window, text="Back", width=25,
            bg="#3f6fb0", fg="white",
            command=self.todo_menu
        ).pack(pady=10)

    def mark_done(self):
        i = simpledialog.askinteger("Done", "Task number")
        if i is not None:
            tasks = self.backend.get_tasks(self.current_user)
            if 1 <= i <= len(tasks):
                self.backend.toggle_task(self.current_user, i - 1)
                messagebox.showinfo("Done", "Task status toggled")
            else:
                messagebox.showerror("Error", "Invalid task number")

    def delete_task(self):
        i = simpledialog.askinteger("Delete", "Task number")
        if i is not None:
            tasks = self.backend.get_tasks(self.current_user)
            if 1 <= i <= len(tasks):
                self.backend.delete_task(self.current_user, i - 1)
                messagebox.showinfo("Done", "Task deleted")
            else:
                messagebox.showerror("Error", "Invalid task number")

TodoApp_Gui()