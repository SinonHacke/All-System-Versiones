import tkinter as tk
from tkinter import messagebox
from datetime import date

# =========================
# IN-MEMORY DATABASE
# =========================
USERS = {}        # username -> password
ATTENDANCE = {}   # username -> attendance stats


class AttendanceApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Attendance System")
        self.window.geometry("480x600")
        self.window.config(bg="#d0e2f2")

        self.current_user = None
        self.selected_status = tk.StringVar()

        self.login_screen()
        self.window.mainloop()

    # -------- HEADER --------
    def create_header(self, text):
        header = tk.Frame(self.window, bg="#3f6fb0", height=110)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text=text,
            fg="white",
            bg="#3f6fb0",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=20)

    # -------- CLEAR --------
    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # =========================
    # LOGIN
    # =========================
    def login_screen(self):
        self.clear()
        self.create_header("Login")

        container = tk.Frame(self.window, bg="#d0e2f2")
        container.pack(expand=True)

        tk.Label(container, text="Username:", bg="#d0e2f2").pack(pady=5)
        self.login_username = tk.Entry(container, width=25)
        self.login_username.pack(pady=5)

        tk.Label(container, text="Password:", bg="#d0e2f2").pack(pady=5)
        self.login_password = tk.Entry(container, show="*", width=25)
        self.login_password.pack(pady=5)

        tk.Button(
            container, text="Log In", width=18,
            command=self.login_user,
            bg="#3f6fb0", fg="white"
        ).pack(pady=15)

        tk.Button(
            container, text="Sign Up", width=18,
            command=self.signup_screen
        ).pack(pady=5)

    def login_user(self):
        username = self.login_username.get()
        password = self.login_password.get()

        if username in USERS and USERS[username] == password:
            self.current_user = username

            if username not in ATTENDANCE:
                ATTENDANCE[username] = {
                    "Present": 0,
                    "Absent": 0,
                    "Excused": 0,
                    "Bonus": False,
                    "last_mark": ""
                }

            self.attendance_screen()
        else:
            messagebox.showerror("Error", "Wrong username or password")

    # =========================
    # SIGN UP
    # =========================
    def signup_screen(self):
        self.clear()
        self.create_header("Sign Up")

        container = tk.Frame(self.window, bg="#d0e2f2")
        container.pack(expand=True)

        tk.Label(container, text="New Username:", bg="#d0e2f2").pack(pady=5)
        self.signup_username = tk.Entry(container, width=25)
        self.signup_username.pack(pady=5)

        tk.Label(container, text="New Password:", bg="#d0e2f2").pack(pady=5)
        self.signup_password = tk.Entry(container, show="*", width=25)
        self.signup_password.pack(pady=5)

        tk.Button(
            container, text="Create Account", width=18,
            command=self.create_user,
            bg="#3f6fb0", fg="white"
        ).pack(pady=15)

        tk.Button(
            container, text="Back to Login", width=18,
            command=self.login_screen
        ).pack()

    def create_user(self):
        username = self.signup_username.get()
        password = self.signup_password.get()

        if username in USERS:
            messagebox.showerror("Error", "Username already exists!")
            return

        USERS[username] = password
        ATTENDANCE[username] = {
            "Present": 0,
            "Absent": 0,
            "Excused": 0,
            "Bonus": False,
            "last_mark": ""
        }

        messagebox.showinfo("Success", "Account created!")
        self.login_screen()

    # =========================
    # ATTENDANCE
    # =========================
    def attendance_screen(self):
        self.clear()
        self.create_header(f"Welcome {self.current_user}")

        container = tk.Frame(self.window, bg="#d0e2f2")
        container.pack(expand=True)

        for text, color in [
            ("Present", "#4caf50"),
            ("Absent", "#f44336"),
            ("Excused", "#ff9800")
        ]:
            tk.Radiobutton(
                container,
                text=text,
                variable=self.selected_status,
                value=text,
                indicatoron=False,
                bg=color, fg="white",
                width=22, pady=5
            ).pack(pady=8)

        self.submit_btn = tk.Button(
            container, text="Submit", width=22,
            command=self.submit_attendance,
            bg="#3f6fb0", fg="white",
            state="disabled"
        )
        self.submit_btn.pack(pady=10)

        self.selected_status.trace(
            "w", lambda *args: self.submit_btn.config(state="normal")
        )

        tk.Button(
            container, text="View Stats", width=22,
            command=self.stats_screen
        ).pack(pady=12)

        tk.Button(
            container, text="Log Out", width=22,
            command=self.login_screen
        ).pack()

    def submit_attendance(self):
        status = self.selected_status.get()
        stats = ATTENDANCE[self.current_user]

        today = str(date.today())
        if stats["last_mark"] == today:
            messagebox.showerror("Error", "Already marked today")
            return

        stats[status] += 1
        stats["last_mark"] = today

        if stats["Present"] >= 7 and stats["Absent"] == 0:
            stats["Bonus"] = True

        self.stats_screen()

    # =========================
    # STATS
    # =========================
    def stats_screen(self):
        self.clear()
        self.create_header(f"{self.current_user} - Stats")

        stats = ATTENDANCE[self.current_user]
        total = stats["Present"] + stats["Absent"] + stats["Excused"]
        total = total if total > 0 else 1

        colors = {
            "Present": "#4caf50",
            "Absent": "#f44336",
            "Excused": "#ff9800"
        }

        for key in ["Present", "Absent", "Excused"]:
            tk.Label(
                self.window,
                text=f"{key}: {stats[key]} ({(stats[key]/total)*100:.1f}%)",
                font=("Segoe UI", 14),
                fg=colors[key],
                bg="#d0e2f2"
            ).pack(pady=5)

        bonus = "Yes 🎉" if stats["Bonus"] else "No"
        tk.Label(
            self.window,
            text=f"Bonus: {bonus}",
            font=("Segoe UI", 16),
            bg="#d0e2f2"
        ).pack(pady=15)

        tk.Button(
            self.window, text="Back", width=22,
            command=self.attendance_screen
        ).pack(pady=10)


# =========================
# RUN
# =========================
AttendanceApp()
