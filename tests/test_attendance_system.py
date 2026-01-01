import unittest
from datetime import date


class AttendanceSystem:
    def __init__(self):
        self.attendance_records = {}

    def login(self, username, password):
        if username == "admin" and password == "1234":
            return True
        return False

    def mark_attendance(self, student_id, day):
        key = (student_id, day)
        if key in self.attendance_records:
            return False  # duplicate
        self.attendance_records[key] = "Present"
        return True

    def get_attendance(self, student_id):
        return [
            record for record in self.attendance_records
            if record[0] == student_id
        ]



class TestAttendanceSystem(unittest.TestCase):

    def setUp(self):
        self.system = AttendanceSystem()

    
    def test_login_valid(self):
        result = self.system.login("admin", "1234")
        self.assertTrue(result)

    def test_login_invalid(self):
        result = self.system.login("admin", "wrong")
        self.assertFalse(result)

    
    def test_mark_attendance_success(self):
        today = date.today()
        result = self.system.mark_attendance("S001", today)
        self.assertTrue(result)

    def test_mark_attendance_duplicate(self):
        today = date.today()
        self.system.mark_attendance("S001", today)
        result = self.system.mark_attendance("S001", today)
        self.assertFalse(result)

    def test_view_attendance(self):
        today = date.today()
        self.system.mark_attendance("S001", today)
        records = self.system.get_attendance("S001")
        self.assertEqual(len(records), 1)


if __name__ == "__main__":
    unittest.main()
