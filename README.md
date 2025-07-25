# FlexiHire Django Backend

Welcome to the **FlexiHire Django Backend**, the server-side component for the FlexiHire Flutter app. This backend handles user authentication (login, registration, logout) and job management (create, read, update, delete) using Django and Firebase Firestore. The system provides a clean, secure, and responsive API for the Flutter frontend, with a modern dashboard interface for job postings.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Firebase Configuration](#firebase-configuration)


## Project Overview
FlexiHire is a job posting platform where users can register, log in, post jobs, edit/delete their own jobs, and search for job listings. The Django backend manages user authentication using Django’s built-in auth system and stores job data in Firebase Firestore. The dashboard interface is designed to be simple, attractive, and user-friendly, with a clean UI featuring a minimal teal accent color (`#00d4c0`), responsive layout, and fading alerts.

## Features
- **User Authentication**:
  - Register with username, email, and password.
  - Login with username and password.
  - Logout functionality.
- **Job Management**:
  - Create job postings with category, title, specifications, and application link.
  - View all jobs in a responsive table with search functionality.
  - Edit or delete jobs (restricted to the job’s creator).
- **UI/UX**:
  - Clean, minimal design with a white background and teal accents.
  - Responsive sidebar with Dashboard, Post Job, and Logout links.
  - Toggleable job creation form with floating labels and placeholders.
  - Success/error messages fade out after 2 seconds.
  - Accessible with ARIA labels and keyboard navigation.
- **Firebase Integration**:
  - Stores job data in Firestore’s `jobs` collection.
  - Secure user-based access control for job edits/deletes.

## Technologies
- **Backend**: Django 4.x, Python 3.8+
- **Database**: Firebase Firestore
- **Frontend Templates**: HTML, CSS, JavaScript
  - Poppins font (Google Fonts)
  - Font Awesome 5.15.4 for icons
- **Dependencies**:
  - `django`: Web framework
  - `python-dotenv`: Environment variable management
  - `firebase-admin`: Firebase Firestore integration
- **Deployment**: Local development server (extendable to production with Gunicorn/Nginx)

## Prerequisites
- **Python 3.8+**: Install from [python.org](https://www.python.org/downloads/).
- **pip**: Python package manager.
- **Virtualenv**: For isolated Python environments.
- **Firebase Account**: Required for Firestore setup.
- **Git**: For cloning the repository.
- **Flutter**: For frontend integration (optional for backend setup).

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BraisonWabwire/flexi_hire_backend.git
   cd flexi_hire_backend
   python -m venv env
   ```
2. **Activate Virtual Environment**:
   ```bash
     source env/bin/activate  # Linux/Mac
     env\Scripts\activate  # Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install django python-dotenv firebase-admin
   ```
4. **Apply Migrations**:
  ```bash
    python manage.py makemigrations
    python manage.py migrate
  ```
5. **Run the Development Server**:
    ```bash
    Python manage.py runserver
    ```
**Access at http://localhost:8000**

## Project Structure
```
flexi_hire_backend/
├── flexi_hire_backend/
│   ├── templates/flexi_hire_backend/
│   │   ├── home.html        # Dashboard with job listings and form
│   │   ├── login.html       # Login page
│   │   ├── register.html    # Registration page
│   │   ├── edit_job.html    # Job editing page
│   ├── forms.py             # JobForm for job creation/editing
│   ├── views.py             # Authentication and job management views
│   ├── urls.py              # URL routing
│   ├── settings.py          # Django settings with Firebase config
├── serviceAccountKey.json   # Firebase credentials
├── .env                     # Environment variables
├── manage.py                # Django management script
├── README.md                # This file
```
## Firebase Configuration
1. **Create a Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/).
   - Create a project named `FlexiHire`.
   - Enable Firestore in "Test Mode" for initial setup.

2. **Download Service Account Key**:
   - In Firebase Console, go to Project Settings > Service Accounts.
   - Generate a new private key (`serviceAccountKey.json`).
   - Place it at `/home/braison-wabwire/Desktop/flutter codes/tasking_app/django_flexi_hire/serviceAccountKey.json`.

3. **Update Firestore Security Rules**:
   In Firebase Console > Firestore > Rules, set:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /jobs/{jobId} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.uid == resource.data.user_id;
    }
  }
}
```




