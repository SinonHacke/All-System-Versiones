import tkinter as tk
from tkinter import messagebox, simpledialog

# -----------------------
# Library Backend (IN MEMORY ONLY)
# -----------------------
class LibraryBackend:
    def __init__(self):
        self.books = {}     # book_id -> {title, author, status}
        self.users = {}     # user_id -> {name, borrowed}
        self.next_book_id = 1
        self.next_user_id = 1

    # ---- BOOK FUNCTIONS ----
    def add_book(self, title, author):
        book_id = self.next_book_id
        self.books[book_id] = {
            "title": title,
            "author": author,
            "status": "available"
        }
        self.next_book_id += 1
        return book_id

    def list_books(self):
        return self.books

    # ---- USER FUNCTIONS ----
    def add_user(self, name):
        user_id = self.next_user_id
        self.users[user_id] = {
            "name": name,
            "borrowed": []
        }
        self.next_user_id += 1
        return user_id

    def list_users(self):
        return self.users

    # ---- BORROW / RETURN ----
    def borrow_book(self, user_id, book_id):
        if user_id not in self.users:
            return False, "User not found"
        if book_id not in self.books:
            return False, "Book not found"

        book = self.books[book_id]
        if book["status"] != "available":
            return False, "Book not available"

        book["status"] = "borrowed"
        self.users[user_id]["borrowed"].append(book_id)
        return True, "Book borrowed successfully"

    def return_book(self, user_id, book_id):
        if user_id not in self.users:
            return False, "User not found"
        if book_id not in self.books:
            return False, "Book not found"
        if book_id not in self.users[user_id]["borrowed"]:
            return False, "This user did not borrow this book"

        self.users[user_id]["borrowed"].remove(book_id)
        self.books[book_id]["status"] = "available"
        return True, "Book returned successfully"

#boda

# -----------------------
# Library GUI
# -----------------------
class LibraryApp:
    def __init__(self):
        self.library = LibraryBackend()

        self.window = tk.Tk()
        self.window.title("Library Management System")
        self.window.geometry("500x600")
        self.window.config(bg="#d0e2f2")

        self.menu()
        self.window.mainloop()

    # ---- Helpers ----
    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def header(self, text):
        frame = tk.Frame(self.window, bg="#3f6fb0", height=80)
        frame.pack(fill="x")
        frame.pack_propagate(False)
        tk.Label(frame, text=text, font=("Segoe UI", 20, "bold"),
                 fg="white", bg="#3f6fb0").pack(pady=20)

    # ---- Main Menu ----
    def menu(self):
        self.clear()
        self.header("Library Menu")

        frame = tk.Frame(self.window, bg="#d0e2f2")
        frame.pack(expand=True)

        tk.Button(frame, text="Add Book", width=30, command=self.add_book).pack(pady=8)
        tk.Button(frame, text="List Books", width=30, command=self.list_books).pack(pady=8)
        tk.Button(frame, text="Add User", width=30, command=self.add_user).pack(pady=8)
        tk.Button(frame, text="List Users", width=30, command=self.list_users).pack(pady=8)
        tk.Button(frame, text="Borrow Book", width=30, command=self.borrow_book).pack(pady=8)
        tk.Button(frame, text="Return Book", width=30, command=self.return_book).pack(pady=8)

    # ---- GUI Actions ----
    def add_book(self):
        title = simpledialog.askstring("Add Book", "Book Title:")
        if not title:
            return
        author = simpledialog.askstring("Add Book", "Author:") or "Unknown"
        book_id = self.library.add_book(title, author)
        messagebox.showinfo("Success", f"Book added with ID {book_id}")

    def list_books(self):
        self.clear()
        self.header("Books")

        frame = tk.Frame(self.window, bg="#d0e2f2")
        frame.pack(fill="both", expand=True)

        books = self.library.list_books()
        if not books:
            tk.Label(frame, text="No books available", bg="#d0e2f2").pack(pady=10)

        for book_id, book in books.items():
            text = f"[{book_id}] {book['title']} - {book['author']} ({book['status']})"
            tk.Label(frame, text=text, bg="#d0e2f2",
                     font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=3)

        tk.Button(frame, text="Back", command=self.menu).pack(pady=10)

    def add_user(self):
        name = simpledialog.askstring("Add User", "User Name:")
        if not name:
            return
        user_id = self.library.add_user(name)
        messagebox.showinfo("Success", f"User added with ID {user_id}")

    def list_users(self):
        self.clear()
        self.header("Users")

        frame = tk.Frame(self.window, bg="#d0e2f2")
        frame.pack(fill="both", expand=True)

        users = self.library.list_users()
        if not users:
            tk.Label(frame, text="No users found", bg="#d0e2f2").pack(pady=10)

        for user_id, user in users.items():
            borrowed = ", ".join(map(str, user["borrowed"])) if user["borrowed"] else "None"
            text = f"[{user_id}] {user['name']} | Borrowed: {borrowed}"
            tk.Label(frame, text=text, bg="#d0e2f2",
                     font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=3)

        tk.Button(frame, text="Back", command=self.menu).pack(pady=10)

    def borrow_book(self):
        user_id = simpledialog.askinteger("Borrow Book", "User ID:")
        book_id = simpledialog.askinteger("Borrow Book", "Book ID:")
        if user_id is None or book_id is None:
            return
        ok, msg = self.library.borrow_book(user_id, book_id)
        messagebox.showinfo("Result", msg)

    def return_book(self):
        user_id = simpledialog.askinteger("Return Book", "User ID:")
        book_id = simpledialog.askinteger("Return Book", "Book ID:")
        if user_id is None or book_id is None:
            return
        ok, msg = self.library.return_book(user_id, book_id)
        messagebox.showinfo("Result", msg)


# -----------------------
# Run Program
# -----------------------
if __name__ == "__main__":
    LibraryApp()
