from todo_backend import TodoListBackend, load_data

def test_load_data(tmp_path):
    p = tmp_path / "todo.json"
    data = load_data(str(p))
    assert "users" in data
    assert "todo" in data

def test_add_task(tmp_path):
    p = tmp_path / "todo.json"
    b = TodoListBackend(str(p))
    b.add_task("ahmed", "Study")
    b2 = TodoListBackend(str(p))
    t = b2.get_tasks("ahmed")
    assert len(t) == 1
    assert t[0]["title"] == "Study"
    assert t[0]["done"] is False

def test_toggle_task(tmp_path):
    p = tmp_path / "todo.json"
    b = TodoListBackend(str(p))
    b.add_task("ahmed", "Task1")
    b.toggle_task("ahmed", 0)
    t = b.get_tasks("ahmed")
    assert t[0]["done"] is True

def test_delete_task(tmp_path):
    p = tmp_path / "todo.json"
    b = TodoListBackend(str(p))
    b.add_task("ahmed", "A")
    b.add_task("ahmed", "B")
    b.delete_task("ahmed", 0)
    t = b.get_tasks("ahmed")
    assert len(t) == 1
    assert t[0]["title"] == "B"