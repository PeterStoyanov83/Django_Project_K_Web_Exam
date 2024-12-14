# Project K - IT and Business Education Platform


## Deployed at
[https://project-k-web.onrender.com/](https://project-k-web.onrender.com/)


## Test Access
- **Normal User**: Limited access.
  - Username: `normaluser`
  - Password: `normie23`
- **Moderator**: Can modify users, lecturers, and courses.
  - Username: `peter`
  - Password: `peterko123`
- **Admin**: Full access to admin panel.
  - Username: `admin`
  - Password: `admin123123`

Admin Panel: [https://project-k-web.onrender.com/admin/](https://project-k-web.onrender.com/admin/) (admin login required).

## Additional Resources
- [Test Report (85% coverage)](https://github.com/PeterStoyanov83/Django_Project_K_Web_Exam/blob/main/TestReport.md)
- [URL Map](https://github.com/PeterStoyanov83/Django_Project_K_Web_Exam/blob/main/URLs.md)
- [Database Representation](https://www.mermaidchart.com/raw/3e142088-efce-4272-90d2-f54fcff318f4?theme=light&version=v0.1&format=svg)


## Overview
Project K is a Django-based IT and business education platform designed to connect students with expert instructors, manage course schedules, track resources, and facilitate administrative tasks. It features a flexible user system, comprehensive course management, and AI-powered chatbot integration for enhanced user support.

## Features

### User Management
- **Custom User Model**: Extends Django's default user model with fields like phone number, profile picture, user type (private/business), and personal/business information.
- **Client Model**: Tracks business clients with company-specific details and registration dates.

### File Management
- **Client File Model**: Enables file upload, storage, and tracking.

### Equipment Tracking
- **Laptop Model**: Tracks laptops assigned to clients with details like brand, serial number, and status (active, maintenance, retired).

### Course Management
- **Lecturer Model**: Represents instructors with detailed profiles and multi-course assignments.
- **Course Model**: Stores details like title, description, capacity, and associated lecturer, room, and calendar events.
- **Time Slot Model**: Manages scheduling with start and end times.
- **Room Model**: Tracks physical/virtual spaces for courses with capacity information.
- **Course Schedule Model**: Links courses to rooms and times, manages recurring events, and auto-creates calendar events.

### Booking and Application System
- **Course Application Model**: Allows course applications and tracks statuses (pending, approved, rejected).
- **Booking Model**: Ensures valid bookings and prevents scheduling conflicts.

### Calendar Integration
- **Calendar and Event Models**: Automatically create and update course sessions.

### Key Features
1. Flexible user system for private and business clients.
2. Comprehensive course scheduling with room allocation.
3. Automated calendar integration for seamless management.
4. Application and booking systems with status tracking.
5. Equipment tracking for business clients.
6. File upload and management capabilities.
7. Capacity and status management for courses, rooms, and schedules.
8. AI-powered chatbot assistant for user support.

## Technology Stack
- Django 4.2.3
- Python 3.8+
- PostgreSQL
- HTML5, CSS3, JavaScript, Tailwind CSS
- Docker for database containerization
- OpenAI API for chatbot (Daisy)

## Local Setup and Installation
1. Clone the repository.
2. Set up a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`.
4. Configure the PostgreSQL database.
5. Run migrations: `python manage.py migrate`.
6. Create a superuser: `python manage.py createsuperuser`.
7. Start the development server: `python manage.py runserver`.
8. Populate sample data: `python manage.py populate_db`.


