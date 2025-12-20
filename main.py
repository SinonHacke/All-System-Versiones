import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import json

USER_FILE = "users.json"

if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        USERS = json.load(f)
else:
    USERS = {}

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
FONT_TITLE = ("Arial", 20, "bold")
FONT_LABEL = ("Arial", 12)
FONT_ENTRY = ("Arial", 12)
FONT_BUTTON = ("Arial", 12)
BUTTON_WIDTH = 20
PAD_Y = 10
BG_COLOR = "#d6e3f8"
HEADER_COLOR = "#4a6fa5"
BUTTON_COLOR = "#4a6fa5"
BUTTON_FG = "white"

def run_python_file(filename):
    filepath = os.path.join(os.getcwd(), filename)
    if os.path.exists(filepath):
        subprocess.run(["python3", filepath])
    else:
        messagebox.showerror("Error", f"File {filename} not found!\nSearched at: {filepath}")

def system_login(system_name, file_to_run):
    login_win = tk.Toplevel()
    login_win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    login_win.resizable(False, False)
    login_win.configure(bg=BG_COLOR)
    login_win.title(f"{system_name} Login")

    header = tk.Label(login_win, text="Login", font=FONT_TITLE, bg=HEADER_COLOR, fg="white")
    header.pack(fill="x", pady=10)

    login_frame = tk.Frame(login_win, bg=BG_COLOR)
    login_frame.pack(pady=30)

    tk.Label(login_frame, text="Username:", font=FONT_LABEL, bg=BG_COLOR).pack(pady=5)
    entry_user = tk.Entry(login_frame, font=FONT_ENTRY)
    entry_user.pack(pady=5)

    tk.Label(login_frame, text="Password:", font=FONT_LABEL, bg=BG_COLOR).pack(pady=5)
    entry_pass = tk.Entry(login_frame, font=FONT_ENTRY, show="*")
    entry_pass.pack(pady=5)

    def check_login():
        username = entry_user.get()
        password = entry_pass.get()
        if username in USERS and USERS[username] == password:
            messagebox.showinfo("Login", f"Welcome {username}!")
            login_win.destroy()
            run_python_file(file_to_run)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    tk.Button(login_frame, text="Log In", font=FONT_BUTTON, width=BUTTON_WIDTH,
              bg=BUTTON_COLOR, fg=BUTTON_FG, command=check_login).pack(pady=PAD_Y)

    def sign_up_window():
        signup = tk.Toplevel(login_win)
        signup.title("Sign Up")
        signup.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        signup.resizable(False, False)
        signup.configure(bg=BG_COLOR)

        header = tk.Label(signup, text="Sign Up", font=FONT_TITLE, bg=HEADER_COLOR, fg="white")
        header.pack(fill="x", pady=10)

        tk.Label(signup, text="Username:", font=FONT_LABEL, bg=BG_COLOR).pack(pady=5)
        new_user = tk.Entry(signup, font=FONT_ENTRY)
        new_user.pack(pady=5)

        tk.Label(signup, text="Password:", font=FONT_LABEL, bg=BG_COLOR).pack(pady=5)
        new_pass = tk.Entry(signup, font=FONT_ENTRY, show="*")
        new_pass.pack(pady=5)

        def create_account():
            username = new_user.get()
            password = new_pass.get()
            if username in USERS:
                messagebox.showerror("Error", "Username already exists")
            elif username == "" or password == "":
                messagebox.showerror("Error", "Username and password cannot be empty")
            else:
                USERS[username] = password
                with open(USER_FILE, "w") as f:
                    json.dump(USERS, f)
                messagebox.showinfo("Success", "Account created successfully!")
                signup.destroy()

        tk.Button(signup, text="Create Account", font=FONT_BUTTON, width=BUTTON_WIDTH,
                  bg=BUTTON_COLOR, fg=BUTTON_FG, command=create_account).pack(pady=PAD_Y)

    tk.Button(login_frame, text="Sign Up", font=FONT_BUTTON, width=BUTTON_WIDTH,
              bg="gray", fg="white", command=sign_up_window).pack(pady=PAD_Y)

def open_menu():
    menu_window = tk.Toplevel()
    menu_window.title("All Systems Menu")
    menu_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    menu_window.resizable(False, False)
    menu_window.configure(bg=BG_COLOR)

    tk.Label(menu_window, text="All Systems Menu", font=FONT_TITLE, bg=BG_COLOR).pack(pady=20)

    systems = [
        ("Attendance System", "Attendance_System.py"),
        ("Library System", "Library_Sysytem.py"),
        ("Todo List System (Updated)", "todolist update.py")
    ]

    for name, file in systems:
        tk.Button(menu_window, text=name, width=BUTTON_WIDTH, bg=BUTTON_COLOR, fg=BUTTON_FG,
                  command=lambda n=name, f=file: system_login(n, f)).pack(pady=PAD_Y)

    tk.Button(menu_window, text="Exit", width=BUTTON_WIDTH, bg="gray", fg="white", command=menu_window.destroy).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  
    open_menu()
    root.mainloop()
