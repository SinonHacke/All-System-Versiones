import json
import os

DATA_FILE = "todo_data.json"

def load_data(data_file=DATA_FILE):
    if not os.path.exists(data_file):
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump({"users": {}, "todo": {}}, f, indent=4)
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "users" not in data:
        data["users"] = {}
    if "todo" not in data:
        data["todo"] = {}
    return data

def save_data(data, data_file=DATA_FILE):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class TodoListBackend:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.data = load_data(self.data_file)

    def create_user(self, username, password):
        username = (username or "").strip()
        password = (password or "").strip()
        if username == "" or password == "":
            return False
        if username in self.data["users"]:
            return False
        self.data["users"][username] = password
        save_data(self.data, self.data_file)
        return True

    def validate_login(self, username, password):
        return username in self.data["users"] and self.data["users"][username] == password

    def get_tasks(self, user):
        return self.data["todo"].get(user, [])

    def add_task(self, user, title):
        self.data["todo"].setdefault(user, [])
        self.data["todo"][user].append({"title": title, "done": False})
        save_data(self.data, self.data_file)

    def toggle_task(self, user, idx):
        self.data["todo"][user][idx]["done"] = not self.data["todo"][user][idx]["done"]
        save_data(self.data, self.data_file)

    def delete_task(self, user, idx):
        self.data["todo"][user].pop(idx)
        save_data(self.data, self.data_file)