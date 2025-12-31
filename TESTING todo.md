# Testing Documentation - To-Do List System

This document outlines the software testing strategy and test cases for the **To-Do List Module**, derived from the system's Use Case Diagram.

---

## Test Objectives
The primary goals of this testing phase are:
* **Functionality Verification:** To ensure that all core features (Add, Edit, Delete, Mark Completed) work according to requirements.
* **Flow Validation:** To confirm the logical sequence from starting the application to viewing all tasks.
* **System Reliability:** To ensure that extended features (Edit/Delete) do not break the main task list.
* **User Experience:** To guarantee a smooth and intuitive interface for the end-user.

---

## 🧪 2. Testing Methodology & Types
The following testing types were applied to ensure comprehensive coverage:

* **Black Box Testing:** Testing the application interface without looking at the internal code structure, focusing purely on inputs and outputs.
* **Functional Testing:** Verifying each specific function (e.g., adding a task) against the functional requirements.
* **Manual Testing:** Executing test steps manually to simulate real-world user behavior.
* **Integration Testing:** Checking the relationship between "Adding a Task" and the "View All Tasks" list to ensure data flows correctly.
* **Regression Testing:** Ensuring that editing or deleting a task does not impact the remaining list of tasks.

---

## 📋 3. Test Cases (Ready for TestRail Import)

| ID | Feature | Test Case Title | Steps | Expected Result | Priority |
|:---|:---|:---|:---|:---|:---|
| **TC-01** | Start App | **Initialize Application** | 1. Launch the To-Do List application. | Main dashboard is displayed with an empty state or task list. | High |
| **TC-02** | Add Task | **Add New Task** | 1. Click 'Add Task'.<br>2. Enter a valid task name.<br>3. Save. | Task is successfully added and visible in the list. | High |
| **TC-03** | Edit Task | **Edit Existing Task** | 1. Select a specific task.<br>2. Click 'Edit'.<br>3. Modify name.<br>4. Save. | Task details are updated instantly in the UI. | Medium |
| **TC-04** | Delete Task | **Remove Task** | 1. Select a task.<br>2. Click 'Delete'.<br>3. Confirm deletion. | Task is removed from the list and database. | Medium |
| **TC-05** | Complete Task| **Mark as Completed** | 1. Locate an active task.<br>2. Click 'Mark Completed'. | Task status changes to 'Done' (visually checked/strikethrough). | High |
| **TC-06** | View All | **Display All Tasks** | 1. Navigate to 'View All Tasks'. | All active and completed tasks are listed correctly. | Low |

---

## 🛠 4. Environment & Tools
* **Test Management Tool:** [TestRail](https://www.gurock.com/testrail/)
* **Version Control:** GitHub
* **Design Reference:** Use Case Diagram (included in project documentation)
