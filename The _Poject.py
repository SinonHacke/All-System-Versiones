import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os
from datetime import date

DATA_FILE = "attendance_library_data.json"

# -----------------------
# Data file init + helpers
# -----------------------
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({
            "users": {},
            "attendance": {},
            "library": {
                "books": {},          # book_id -> {title, author, status}
                "library_users": {},  # lib_user_id -> {name, borrowed: [book_ids]}
                "next_book_id": 1,
                "next_lib_user_id": 1
            }
        }, f, indent=4)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------
# Library backend classes (light wrappers)
# -----------------------
class LibraryBackend:
    def __init__(self):
        self.data = load_data()
        self.lib = self.data["library"]

    def add_book(self, title, author):
        bid = self.lib["next_book_id"]
        self.lib["books"][str(bid)] = {"title": title, "author": author, "status": "available"}
        self.lib["next_book_id"] += 1
        save_data(self.data)
        return bid

    def list_books(self):
        return self.lib["books"]

    def remove_book(self, book_id):
        book_id = str(book_id)
        if book_id in self.lib["books"]:
            # prevent removing if borrowed
            if self.lib["books"][book_id]["status"] == "borrowed":
                return False, "Book is currently borrowed."
            del self.lib["books"][book_id]
            save_data(self.data)
            return True, "Removed."
        return False, "Not found."

    def add_library_user(self, name):
        uid = self.lib["next_lib_user_id"]
        self.lib["library_users"][str(uid)] = {"name": name, "borrowed": []}
        self.lib["next_lib_user_id"] += 1
        save_data(self.data)
        return uid

    def list_library_users(self):
        return self.lib["library_users"]

    def borrow_book(self, lib_user_id, book_id):
        lib_user_id = str(lib_user_id)
        book_id = str(book_id)
        if lib_user_id not in self.lib["library_users"]:
            return False, "Library user not found."
        if book_id not in self.lib["books"]:
            return False, "Book not found."
        book = self.lib["books"][book_id]
        if book["status"] != "available":
            return False, "Book is not available."
        # Borrow
        book["status"] = "borrowed"
        self.lib["library_users"][lib_user_id]["borrowed"].append(book_id)
        save_data(self.data)
        return True, "Borrowed successfully."

    def return_book(self, lib_user_id, book_id):
        lib_user_id = str(lib_user_id)
        book_id = str(book_id)
        if lib_user_id not in self.lib["library_users"]:
            return False, "Library user not found."
        if book_id not in self.lib["books"]:
            return False, "Book not found."
        if book_id not in self.lib["library_users"][lib_user_id]["borrowed"]:
            return False, "This user did not borrow this book."
        # Return
        self.lib["library_users"][lib_user_id]["borrowed"].remove(book_id)
        self.lib["books"][book_id]["status"] = "available"
        save_data(self.data)
        return True, "Returned successfully."

# -----------------------
# Main App (Tkinter)
# -----------------------
class AttendanceLibraryApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Attendance & Library System")
        self.window.geometry("520x650")
        self.window.config(bg="#d0e2f2")
        self.window.resizable(True, True)

        self.current_user = None
        self.selected_status = tk.StringVar()
        self.library = LibraryBackend()

        self.login_screen()
        self.window.mainloop()

    # Header helper
    def create_header(self, text):
        header = tk.Frame(self.window, bg="#3f6fb0", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=text, fg="white", bg="#3f6fb0",
                 font=("Segoe UI", 22, "bold")).pack(pady=18)

    # Clear screen
    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # -----------------------
    # Login / Signup screens
    # -----------------------
    def login_screen(self):
        self.clear()
        self.create_header("Login")
        container = tk.Frame(self.window, bg="#d0e2f2")
        container.pack(expand=True)

        tk.Label(container, text="Username:", font=("Segoe UI", 12), bg="#d0e2f2").pack(pady=5)
        self.login_username = tk.Entry(container, font=("Segoe UI", 12), width=28)
        self.login_username.pack(pady=5)

        tk.Label(container, text="Password:", font=("Segoe UI", 12), bg="#d0e2f2").pack(pady=5)
        self.login_password = tk.Entry(container, show="*", font=("Segoe UI", 12), width=28)
        self.login_password.pack(pady=5)

        tk.Button(container, text="Log In", font=("Segoe UI", 12), width=20,
                  command=self.login_user, bg="#3f6fb0", fg="white",
                  activebackground="#2e4f82").pack(pady=12)
        tk.Button(container, text="Sign Up", font=("Segoe UI", 12), width=20,
                  command=self.signup_screen).pack(pady=6)

    def login_user(self):
        data = load_data()
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        if username in data["users"] and data["users"][username] == password:
            self.current_user = username
            # ensure attendance keys
            if username not in data["attendance"]:
                data["attendance"][username] = {"Present":0,"Absent":0,"Excused":0,"Bonus":False,"last_mark":""}
            else:
                for key in ["Present","Absent","Excused","Bonus","last_mark"]:
                    if key not in data["attendance"][username]:
                        data["attendance"][username][key] = 0 if key in ["Present","Absent","Excused"] else False if key=="Bonus" else ""
            save_data(data)
            self.main_menu()
        else:
            messagebox.showerror("Error", "Wrong username or password")

    def signup_screen(self):
        self.clear()
        self.create_header("Sign Up")
        container = tk.Frame(self.window, bg="#d0e2f2")
        container.pack(expand=True)

        tk.Label(container, text="New Username:", font=("Segoe UI", 12), bg="#d0e2f2").pack(pady=5)
        self.signup_username = tk.Entry(container, font=("Segoe UI", 12), width=28)
        self.signup_username.pack(pady=5)
        tk.Label(container, text="New Password:", font=("Segoe UI", 12), bg="#d0e2f2").pack(pady=5)
        self.signup_password = tk.Entry(container, show="*", font=("Segoe UI", 12), width=28)
        self.signup_password.pack(pady=5)

        tk.Button(container, text="Create Account", font=("Segoe UI", 12), width=20,
                  command=self.create_user, bg="#3f6fb0", fg="white",
                  activebackground="#2e4f82").pack(pady=12)
        tk.Button(container, text="Back to Login", font=("Segoe UI", 12), width=20,
                  command=self.login_screen).pack()

    def create_user(self):
        data = load_data()
        username = self.signup_username.get().strip()
        password = self.signup_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        if username in data["users"]:
            messagebox.showerror("Error", "Username already exists!")
            return

        data["users"][username] = password
        data["attendance"][username] = {"Present":0,"Absent":0,"Excused":0,"Bonus":False,"last_mark":""}
        save_data(data)
        messagebox.showinfo("Success", "Account created!")
        self.login_screen()

    # -----------------------
    # Main menu after login
    # -----------------------
    def main_menu(self):
        self.clear()
        self.create_header(f"Welcome, {self.current_user}")
        container = tk.Frame(self.window, bg="#d0e2f2")
        container.pack(expand=True)

        tk.Button(container, text="Attendance", font=("Segoe UI", 13), width=30,
                  command=self.attendance_screen, bg="#4caf50", fg="white").pack(pady=12)
        tk.Button(container, text="Stats", font=("Segoe UI", 13), width=30,
                  command=self.stats_screen, bg="#3f6fb0", fg="white").pack(pady=12)
        tk.Button(container, text="Library", font=("Segoe UI", 13), width=30,
                  command=self.library_menu, bg="#8e44ad", fg="white").pack(pady=12)
        tk.Button(container, text="Log Out", font=("Segoe UI", 13), width=30,
                  command=self.logout, bg="#f44336", fg="white").pack(pady=12)

    def logout(self):
        self.current_user = None
        self.login_screen()

    # -----------------------
    # Attendance screens
    # -----------------------
    def attendance_screen(self):
        self.clear()
        self.create_header("Attendance")
        container = tk.Frame(self.window, bg="#d0e2f2")
        container.pack(expand=True)

        tk.Radiobutton(container, text="Present", variable=self.selected_status, value="Present",
                       font=("Segoe UI", 12), bg="#4caf50", fg="white",
                       indicatoron=False, width=26, pady=6).pack(pady=8)
        tk.Radiobutton(container, text="Absent", variable=self.selected_status, value="Absent",
                       font=("Segoe UI", 12), bg="#f44336", fg="white",
                       indicatoron=False, width=26, pady=6).pack(pady=8)
        tk.Radiobutton(container, text="Excused Absence", variable=self.selected_status, value="Excused",
                       font=("Segoe UI", 12), bg="#ff9800", fg="white",
                       indicatoron=False, width=26, pady=6).pack(pady=8)

        self.submit_btn = tk.Button(container, text="Submit", font=("Segoe UI", 12), width=26,
                                    command=self.submit_attendance, bg="#3f6fb0", fg="white",
                                    state="disabled")
        self.submit_btn.pack(pady=10)

        self.selected_status.trace("w", lambda *args: self.submit_btn.config(state="normal"))
        tk.Button(container, text="Back to Menu", font=("Segoe UI", 12), width=26,
                  command=self.main_menu).pack(pady=12)

    def submit_attendance(self):
        status = self.selected_status.get()
        if not status:
            messagebox.showerror("Error", "Please select a status before submitting")
            return

        data = load_data()
        if self.current_user not in data["attendance"]:
            data["attendance"][self.current_user] = {"Present":0,"Absent":0,"Excused":0,"Bonus":False,"last_mark":""}
        user_stats = data["attendance"][self.current_user]

        for key in ["Present","Absent","Excused","Bonus","last_mark"]:
            if key not in user_stats:
                user_stats[key] = 0 if key in ["Present","Absent","Excused"] else False if key=="Bonus" else ""

        today = str(date.today())
        if user_stats["last_mark"] == today:
            messagebox.showerror("Error", "Already marked today")
            return

        user_stats[status] += 1
        user_stats["last_mark"] = today
        if user_stats["Present"] >= 7 and user_stats["Absent"] == 0:
            user_stats["Bonus"] = True

        save_data(data)
        messagebox.showinfo("Saved", "Attendance recorded.")
        self.stats_screen()

    # -----------------------
    # Stats screen
    # -----------------------
    def stats_screen(self):
        self.clear()
        self.create_header("Your Stats")
        data = load_data()
        stats = data["attendance"].get(self.current_user, {"Present":0,"Absent":0,"Excused":0,"Bonus":False})
        total = stats["Present"] + stats["Absent"] + stats["Excused"]
        total = total if total > 0 else 1

        colors = {"Present":"#4caf50","Absent":"#f44336","Excused":"#ff9800"}
        frame = tk.Frame(self.window, bg="#d0e2f2")
        frame.pack(expand=True)
        for key in ["Present","Absent","Excused"]:
            tk.Label(frame, text=f"{key}: {stats.get(key,0)} ({(stats.get(key,0)/total)*100:.1f}%)",
                     font=("Segoe UI", 14), fg=colors[key], bg="#d0e2f2").pack(pady=6)

        bonus_text = "Yes 🎉" if stats.get("Bonus") else "No"
        tk.Label(frame, text=f"Bonus: {bonus_text}", font=("Segoe UI", 15), bg="#d0e2f2").pack(pady=12)

        tk.Button(frame, text="Back to Menu", font=("Segoe UI", 12), width=24,
                  command=self.main_menu).pack(pady=10)

    # -----------------------
    # Library GUI screens
    # -----------------------
    def library_menu(self):
        self.clear()
        self.create_header("Library Menu")
        container = tk.Frame(self.window, bg="#d0e2f2")
        container.pack(expand=True)

        tk.Button(container, text="Add Book", font=("Segoe UI", 12), width=28,
                  command=self.add_book_screen, bg="#3f6fb0", fg="white").pack(pady=8)
        tk.Button(container, text="List Books", font=("Segoe UI", 12), width=28,
                  command=self.list_books_screen, bg="#4caf50", fg="white").pack(pady=8)
        tk.Button(container, text="Add Library User", font=("Segoe UI", 12), width=28,
                  command=self.add_library_user_screen, bg="#8e44ad", fg="white").pack(pady=8)
        tk.Button(container, text="List Library Users", font=("Segoe UI", 12), width=28,
                  command=self.list_library_users_screen, bg="#9b59b6", fg="white").pack(pady=8)
        tk.Button(container, text="Borrow Book", font=("Segoe UI", 12), width=28,
                  command=self.borrow_book_screen, bg="#f39c12", fg="white").pack(pady=8)
        tk.Button(container, text="Return Book", font=("Segoe UI", 12), width=28,
                  command=self.return_book_screen, bg="#16a085", fg="white").pack(pady=8)
        tk.Button(container, text="Back to Menu", font=("Segoe UI", 12), width=28,
                  command=self.main_menu, bg="#f44336", fg="white").pack(pady=12)

    def add_book_screen(self):
        title = simpledialog.askstring("Add Book", "Enter book title:", parent=self.window)
        if not title:
            return
        author = simpledialog.askstring("Add Book", "Enter author name:", parent=self.window) or "Unknown"
        bid = self.library.add_book(title, author)
        messagebox.showinfo("Success", f"Book added with ID: {bid}")
        self.library_menu()

    def list_books_screen(self):
        self.clear()
        self.create_header("Books")
        books = self.library.list_books()
        frame = tk.Frame(self.window, bg="#d0e2f2")
        frame.pack(fill="both", expand=True)
        if not books:
            tk.Label(frame, text="No books in library.", font=("Segoe UI", 13), bg="#d0e2f2").pack(pady=10)
        else:
            for bid, info in books.items():
                status = info["status"]
                text = f"[{bid}] {info['title']} by {info['author']} - {status}"
                tk.Label(frame, text=text, font=("Segoe UI", 12), bg="#d0e2f2").pack(anchor="w", padx=10, pady=4)
        tk.Button(frame, text="Back", font=("Segoe UI", 12), width=20, command=self.library_menu).pack(pady=12)

    def add_library_user_screen(self):
        name = simpledialog.askstring("Add Library User", "Enter user name:", parent=self.window)
        if not name:
            return
        uid = self.library.add_library_user(name)
        messagebox.showinfo("Success", f"Library user added with ID: {uid}")
        self.library_menu()

    def list_library_users_screen(self):
        self.clear()
        self.create_header("Library Users")
        users = self.library.list_library_users()
        frame = tk.Frame(self.window, bg="#d0e2f2")
        frame.pack(fill="both", expand=True)
        if not users:
            tk.Label(frame, text="No library users.", font=("Segoe UI", 13), bg="#d0e2f2").pack(pady=10)
        else:
            for uid, info in users.items():
                borrowed = ", ".join(info["borrowed"]) if info["borrowed"] else "None"
                text = f"[{uid}] {info['name']} - Borrowed: {borrowed}"
                tk.Label(frame, text=text, font=("Segoe UI", 12), bg="#d0e2f2").pack(anchor="w", padx=10, pady=4)
        tk.Button(frame, text="Back", font=("Segoe UI", 12), width=20, command=self.library_menu).pack(pady=12)

    def borrow_book_screen(self):
        # ask for IDs
        try:
            lib_user_id = simpledialog.askinteger("Borrow", "Enter Library User ID:", parent=self.window)
            if lib_user_id is None:
                return
            book_id = simpledialog.askinteger("Borrow", "Enter Book ID:", parent=self.window)
            if book_id is None:
                return
        except Exception:
            messagebox.showerror("Error", "Invalid input.")
            return
        ok, msg = self.library.borrow_book(lib_user_id, book_id)
        if ok:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
        self.library_menu()

    def return_book_screen(self):
        try:
            lib_user_id = simpledialog.askinteger("Return", "Enter Library User ID:", parent=self.window)
            if lib_user_id is None:
                return
            book_id = simpledialog.askinteger("Return", "Enter Book ID:", parent=self.window)
            if book_id is None:
                return
        except Exception:
            messagebox.showerror("Error", "Invalid input.")
            return
        ok, msg = self.library.return_book(lib_user_id, book_id)
        if ok:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
        self.library_menu()

# -----------------------
# Run
# -----------------------
if __name__ == "__main__":
    AttendanceLibraryApp()