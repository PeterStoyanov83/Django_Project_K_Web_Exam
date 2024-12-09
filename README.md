# Project K - IT and Business Education Platform

# Deployed at - [https://project-k-web.onrender.com/](https://project-k-web.onrender.com/)


[Test Report - coverage 85%](https://github.com/PeterStoyanov83/Django_Project_K_Web_Exam/blob/main/TestReport.md)


[URL map](https://github.com/PeterStoyanov83/Django_Project_K_Web_Exam/blob/main/URLs.md)


[Full DataBase Representation](https://www.mermaidchart.com/raw/3e142088-efce-4272-90d2-f54fcff318f4?theme=light&version=v0.1&format=svg)


## Overview

Project K is a comprehensive IT and business education platform designed to connect students with expert instructors,
manage course schedules, and facilitate client management. This Django-based web application provides a robust system
for course management, client interactions, and administrative tasks.


The idea started 1 year ago While Peter was enrolled in Keibitz, Basel- an education center for unemployed people 
living in Switzerland. The IT department needed a tool that combines several custom functionalities that couldn't be 
found in ready tools therefore Peter offered to start planning and development of such tool. Using his skills and 
knowledge in Python and Django. Back then Peter wasn't able to complete the full extent of the project since he hadn't 
yet covered the Django Web and Front-end modules in Softuni. 


##  Take A Look Around: 

### log-in with one of these users: 

- Test users :
  - normal user (limited access) Sees most of the app except the Admin Panel 
    - username : normaluser
    - password : normie123

  - Moderator:  (limited access) Can access the app and modify lecturers, courses and users 
    - username : peter
    - password : peterko123    

  - admin user (full access)  Has full admin rights and can access django admin panel 
    - username : admin
    - password : Admin123123
   
      
- Access the admin panel at `https://project-k-web.onrender.com/admin/`
  (you won't be able to access it if you are not logged in as admin)

- Register as a new user or log in
 
- Explore courses, apply for courses, and manage your profile
- Admins can manage users, courses, and applications through the admin interface


## Features

### User Management

- User registration with different user types (Private and Business)
- User authentication and authorization
- User profile management
- Password reset functionality

### Course Management

- Create, read, update, and delete (CRUD) operations for courses
- Course scheduling with room assignments
- View course details and available seats
- Apply for courses (for clients)
- Approve or reject course applications (for admins)
- Interactive course schedule display

### Client Management

- Client profile creation and management
- Distinction between private and business clients
- File upload and management for clients

### Lecturer Management

- CRUD operations for lecturers
- Assign lecturers to courses
- View lecturer details and assigned courses

### Administrative Functions

- Admin panel for managing various aspects of the application
- User management (admin, staff, clients)
- Course application review and approval
- Room management
- Schedule management (still in development)
- Generate reports and analytics

### Booking System

- Students can book available courses
- View and manage bookings
- Cancel bookings


### Resource (Laptop) Management

- Track laptops assigned to clients
- Manage laptop inventory (add, update, delete)

### User Interface

- Responsive design for various devices
- Intuitive navigation and user-friendly forms
- Interactive course schedule display
- Tailwind CSS for modern and clean UI (still trying to implement this fully )

### Email Notifications

- Send confirmation emails for account creation, password reset, etc. (in development)
- Course application status notifications
- Booking confirmations and reminders

### Search and Filter

- Search functionality for courses, users, and other entities
- Filter options for refined search results

### Security

- Secure authentication system
- Password hashing and protection
- CSRF protection
- Proper permission checks for different user roles

### Additional Features

- AI-powered chatbot assistant (Daisy) for user support
- Pagination for long lists (e.g., course list, user list)
- Form validation and error handling
- Responsive design for mobile and desktop views

## Technology Stack

- Django 4.2.3
- Python 3.8+
- PostgreSQL
- HTML5, CSS3, JavaScript
- Tailwind CSS for styling
- Django Scheduler for course scheduling
- Pillow for image processing
- Docker for containerization of the database
- OpenAI API for chatbot functionality (talk to Daisy)

## Local Setup and Installation

1. Clone the repository
2. Set up a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the PostgreSQL database
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`
8. Try data population : `python manage.py populate_db`






