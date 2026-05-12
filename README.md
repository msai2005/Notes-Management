# Notes Management System

A secure and scalable RESTful Notes Management API built using Flask, MySQL, and JWT Authentication. The application allows users to register, authenticate, and manage personal notes securely with complete CRUD operations.

---

## Features

* User Registration & Login Authentication
* JWT-Based Secure Authentication
* Create, Read, Update, and Delete Notes (CRUD)
* Protected REST API Routes
* MySQL Database Integration
* Flask Blueprints & Modular Architecture
* Input Validation & Error Handling
* API Testing using Postman

---

## Tech Stack

### Backend

* Python
* Flask
* REST API
* Flask-JWT-Extended

### Database

* MySQL

### Tools & Technologies

* Postman
* Git & GitHub
* VS Code

---

## Project Structure

```bash
Notes-Management/
│
├── app/
├── routes/
├── models/
├── templates/
├── static/
├── app.py
├── config.py
├── requirements.txt
├── README.md
```

---

## API Endpoints

### Authentication

| Method | Endpoint  | Description         |
| ------ | --------- | ------------------- |
| POST   | /register | Register a new user |
| POST   | /login    | Login user          |

### Notes

| Method | Endpoint    | Description     |
| ------ | ----------- | --------------- |
| GET    | /notes      | Fetch all notes |
| POST   | /notes      | Create new note |
| PUT    | /notes/<id> | Update note     |
| DELETE | /notes/<id> | Delete note     |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/msai2005/Notes-Management.git
```

### Navigate to Project

```bash
cd Notes-Management
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

---

## Authentication

This project uses JWT Authentication for securing protected routes. Users receive an access token after successful login to access Notes APIs securely.

---

## Future Improvements

* Cloud Deployment using Render
* Swagger API Documentation
* Docker Support
* Pagination & Search
* Password Reset Feature

---

## Author

Krishna Sai Mudigonda

* GitHub: https://github.com/msai2005
* LinkedIn: https://linkedin.com/in/krishnasai-mudigonda
