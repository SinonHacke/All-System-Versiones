#  All-System-Versiones

**All-System-Versiones** 
 is a modular system project consisting of three main modules:
1. ToDo List
2. Library Management
3. Attendance Tracking

The project is structured for professional development, testing, CI/CD, and teamwork collaboration.
---
##  Project Idea:
Project Name: All-System-Versiones
Description:
All-System-Versiones is a modular management system that combines multiple core systems into a single professional project. It is designed for modular development, team collaboration, and version-controlled deployment.
Goals:
Create a modular project where each module can work independently.
Provide core management systems: ToDo List, Library Management, and Attendance Tracking.
Enable unit testing and CI/CD pipelines for continuous integration and deployment.
Organize tasks using GitHub Project Board for team collaboration.
Key Features:
Modular architecture for independent system development
Core modules: ToDo, Library, Attendance
Unit and integration testing using Jest
CI/CD with GitHub Actions
Full documentation for professional usage
Team collaboration with GitHub Issues and Project Board
## 1. Project Structure
All-System-Versiones/
├── src/
│ ├── modules/
│ │ ├── todo.js
│ │ ├── library.js
│ │ └── attendance.js
│ ├── tests/
│ │ ├── todo.test.js
│ │ ├── library.test.js
│ │ └── attendance.test.js
│ └── index.js
├── .github/
│ └── workflows/
│ └── ci.yml
├── .gitignore
├── package.json
└── PROJECT_DOC.md
## 2.1 Library Management Module
## project Idea:
Module Name: Library Management
Description:
A system to manage books in a library or personal collection. It handles adding, borrowing, returning, and viewing books, keeping track of which books are borrowed.
Goals:
Keep a record of all books
Track borrowing and returning of books
Prevent borrowing a book that is already borrowed
Provide an easy interface for viewing all books
Core Features:
Add a new book with title and author
Borrow a book (mark it as borrowed)
Return a book (mark it as available)
View all books and their status
Optional Future Enhancements:
Search books by title or author
Track borrowers’ names
Track borrowing history
Example Usage:
Add a book: "1984", "George Orwell"
Borrow a book by ID
Return a book by ID
Display all books with status
File: src/modules/library.js
Features:
Add books
Borrow and return books
View all books
const Library = require("./modules/library");
const lib = new Library();
const book1 = lib.addBook("1984", "George Orwell");
lib.borrowBook(book1.id);
console.log(lib.getBooks());
## 2.2 Attendance Tracking Module

## project Idea
Module Name: Attendance Management
Description:
A system to track attendance of students or employees. It records daily attendance, allows retrieval of individual or overall records, and provides a structured way to monitor presence.
Goals:
Mark attendance for each person per day
View attendance for a specific person
View all attendance records
Keep attendance history in a structured format
Core Features:
Mark attendance for a person (with date automatically assigned)
Retrieve attendance records for a person
Retrieve all attendance records
Store records with unique IDs for tracking
Optional Future Enhancements:
Export attendance to CSV
Generate monthly or weekly reports
Track attendance statistics (present/absent ratio)
Example Usage:
Mark attendance for "Alice" today
Retrieve all attendance records
Retrieve records for a specific person "Bob"
File: src/modules/attendance.js
Features:
Mark attendance for students/employees
View attendance for specific person or all
Example Usage:
const Attendance = require("./modules/attendance");
const att = new Attendance();
att.markAttendance("Alice");
att.markAttendance("Bob");
console.log(att.getAttendance());

##  Project Idea

The goal of this project is to create a modular ToDoList system with core features, including:
- Adding, deleting, updating, and viewing tasks
- Organizing the project on GitHub with a Project Board
- CI/CD setup for running tests and deployment
- Complete project documentation

---

##  2.3 TO-Do list system
The goal of this project is to create a modular ToDoList system with core features, including:
- Adding, deleting, updating, and viewing tasks
- Organizing the project on GitHub with a Project Board
- CI/CD setup for running tests and deployment
- Complete project documentation

##  Features

✔ Add new tasks  
✔ Delete tasks  
✔ Update tasks  
✔ View all tasks with filtering options  
✔ Organize the project with GitHub Project Board  
✔ Unit & Integration testing  
✔ CI/CD using GitHub Actions  
✔ Complete project documentation

---

##  Usage

### 1. Clone the repository
```bash
git clone https://github.com/SinonHacke/All-System-Versiones.git
cd All-System-Versiones
Tasks & Project Board

All current tasks are organized in the GitHub Project Board under columns:

Backlog → To Do → In Progress → Review → Done

CI/CD

GitHub Actions is set up to run:

✔ Install dependencies
✔ Run all tests
✔ Deploy updates automatically

Workflow files are located in:

.github/workflows/

Project Team

Ensure all members have Write / Maintain permissions

Any member can create a new Issue and it will automatically appear in Backlog

Contributing

Open a new Issue if you have a suggestion

Follow the Labeling rules

Submit a Pull Request to the correct branch
