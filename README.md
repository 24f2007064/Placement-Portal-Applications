# Campus Recruitment Management System

## Overview
Managing campus recruitment drives often involves juggling messy spreadsheets, scattered emails, and manual tracking. This project provides a centralized, automated web application designed to streamline the placement process for educational institutes. It offers a structured ecosystem where administrators, hiring companies, and students can interact efficiently without data redundancy or logistical bottlenecks.

## Core Features

### 🛡️ Admin Portal
* **Approval Workflows:** Review and approve/reject new company registrations and job postings to maintain platform quality.
* **System Oversight:** View high-level metrics (active jobs, total applications, placement history).
* **Company Moderation:** Ability to blacklist companies that violate recruitment policies.

### 🏢 Company Portal
* **Job Management:** Create, publish, and close job listings.
* **Applicant Tracking:** View student applications and download resumes.
* **Status Updates:** Move candidates through the pipeline (Shortlist, Reject, Place), automatically generating placement records and logging status history.

### 🎓 Student Portal
* **Profile Management:** Build a comprehensive profile including CGPA, department, and resume links.
* **Job Board:** Search and filter approved, active jobs.
* **Application Dashboard:** One-click apply to opportunities and track real-time application status changes.
* **Notification Center:** Receive automated alerts when a company updates an application status.

## Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLite, Flask-SQLAlchemy (ORM)
* **Frontend:** HTML, CSS, Jinja2 Templating
* **Security:** Werkzeug (Password hashing and verification)

## Database Schema
The application uses a robust relational model to tie all entities together:
* `User` (Admin/Company/Student with Role-Based Access Control)
* Profiles (`StudentProfile`, `CompanyProfile`)
* `Job` & `Application` (Tracks the hiring pipeline)
* `ApplicationStatusLog` (Maintains historical changes)
* `Notification` (Alerts for users)
* `Placement` (Finalized offer records)

## Author
**Anirban Das**  
BS Data Science, IIT Madras | BTech Ceramic Technology, GCECT
