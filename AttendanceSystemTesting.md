# Attendance System Testing

## 1. Testing Objective
The objective of testing is to verify that the Attendance System works correctly, meets the specified requirements, and is free from critical errors. Testing ensures the system is reliable and usable by teachers and students.

---

## 2. Types of Testing Used
The following testing types were applied:

- Unit Testing  
- System Testing  
- User Acceptance Testing (UAT)

---

## 3. Test Cases

### 3.1 Login Test Cases

| Test Case ID | Test Description | Input | Expected Result | Actual Result | Status |
|-------------|-----------------|-------|-----------------|---------------|--------|
| TC-01 | Login with valid credentials | Correct username and password | User logs in successfully | User logged in successfully | Pass |
| TC-02 | Login with invalid password | Incorrect password | Error message displayed | Error message displayed | Pass |
| TC-03 | Login with empty fields | Empty username/password | Login denied | Login denied | Pass |

---

### 3.2 Attendance Management Test Cases

| Test Case ID | Test Description | Input | Expected Result | Actual Result | Status |
|-------------|-----------------|-------|-----------------|---------------|--------|
| TC-04 | Mark attendance | Student marked as Present | Attendance saved | Attendance saved | Pass |
| TC-05 | Duplicate attendance entry | Same student, same date | Duplicate prevented | Duplicate prevented | Pass |
| TC-06 | Mark attendance without date | No date selected | Error message shown | Error message shown | Pass |
| TC-07 | Edit attendance record | Updated attendance status | Record updated | Record updated | Pass |

---

### 3.3 Attendance Report Test Cases

| Test Case ID | Test Description | Input | Expected Result | Actual Result | Status |
|-------------|-----------------|-------|-----------------|---------------|--------|
| TC-08 | View attendance report | Valid class and date | Report displayed | Report displayed | Pass |
| TC-09 | Search attendance by student | Student ID | Correct record shown | Correct record shown | Pass |
| TC-10 | View attendance percentage | Student selected | Correct percentage shown | Correct percentage shown | Pass |

---

### 3.4 Student Access Test Cases

| Test Case ID | Test Description | Input | Expected Result | Actual Result | Status |
|-------------|-----------------|-------|-----------------|---------------|--------|
| TC-11 | Student views own attendance | Student login | Attendance displayed | Attendance displayed | Pass |
| TC-12 | Student tries to edit attendance | Student role | Access denied | Access denied | Pass |

---

## 4. User Acceptance Testing (UAT)

| User | Scenario | Result |
|------|---------|--------|
| Teacher | Mark daily attendance | Accepted |
| Teacher | View attendance report | Accepted |
| Student | View own attendance record | Accepted |

All user acceptance scenarios were successfully completed.

---

## 5. Testing Summary
All major functionalities of the Attendance System were tested successfully. The system meets the functional requirements defined in the backlog and performs as expected without critical issues.

---
