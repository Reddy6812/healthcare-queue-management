# healthcare-queue-management

---

```markdown
# Healthcare Appointment and Queue Management System

A full-stack web application designed to streamline patient scheduling, real-time queue updates, and automated notifications in clinics and hospitals.

---

## Table of Contents

1. [Features](#features)  
2. [Tech Stack](#tech-stack)  
3. [Project Structure](#project-structure)  
4. [Authentication](#authentication)  
5. [Real-Time Queue Updates](#real-time-queue-updates)  
6. [Notifications](#notifications)  
7. [Getting Started](#getting-started)  
8. [API Endpoints](#api-endpoints)  
9. [Admin Panel](#admin-panel)  
10. [Future Enhancements](#future-enhancements)  
11. [License](#license)

---

## Features

- Patient registration and doctor selection  
- Appointment scheduling and live queue management  
- Real-time queue updates via WebSockets  
- JWT-based authentication for patients, doctors, and admins  
- SMS notifications using Twilio when it’s the patient’s turn  
- Notification logs stored in the database  
- Admin dashboard for managing users and queues  
- RESTful APIs using Django REST Framework  
- Dockerized deployment with Docker Compose

---

## Tech Stack

**Backend:**
- Django (REST Framework)
- PostgreSQL
- Redis
- Django Channels (WebSockets)
- Celery (Task queue)
- Twilio (SMS notifications)
- Simple JWT (Authentication)

**Frontend:**
- React (optional for patient/admin dashboards)

**DevOps:**
- Docker, Docker Compose

---

## Project Structure

```
healthcare-queue-management/
├── backend/
│   ├── appointments/         # App logic (models, views, serializers, tasks)
│   ├── healthcare/           # Project config (settings, routing)
│   ├── manage.py
│   ├── requirements.txt
├── frontend/                 # Optional React frontend
├── docker-compose.yml
└── README.md
```

---

## Authentication

- Uses **JWT authentication** via `djangorestframework-simplejwt`
- Role-based access:
  - Patients can register and view queues
  - Admins/staff can manage queues and notify patients
- Token endpoints:
  - `POST /api/token/` → Get access and refresh tokens
  - `POST /api/token/refresh/` → Refresh access token

---

## Real-Time Queue Updates

- **WebSocket Endpoint:**
  ```
  ws://localhost:8000/ws/queue/<doctor_id>/
  ```
- When queue changes (e.g., after notify-next), real-time updates are broadcast to all subscribed clients

---

## Notifications

- SMS notifications are sent using the **Twilio API**
- Triggered when a patient reaches the front of the queue
- Message: `"It is your turn. Please proceed to the doctor's office."`
- All messages are logged in the database under the `Notification` model

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/healthcare-queue-management.git
cd healthcare-queue-management
```

### 2. (Optional) Set Environment Variables

If you use `.env`, or export directly:

```bash
export TWILIO_ACCOUNT_SID=your_account_sid
export TWILIO_AUTH_TOKEN=your_auth_token
export TWILIO_FROM_NUMBER=+1234567890
```

Or hardcode into `settings.py` during development.

### 3. Build Docker Containers

```bash
docker-compose build
```

### 4. Start All Services

```bash
docker-compose up
```

### 5. Create a Superuser for Admin Access

```bash
docker-compose exec backend python manage.py createsuperuser
```

Visit: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## API Endpoints

### Authentication

| Method | Endpoint              | Description               |
|--------|-----------------------|---------------------------|
| POST   | `/api/token/`         | Obtain JWT tokens         |
| POST   | `/api/token/refresh/` | Refresh JWT access token  |

### Core API

| Method | Endpoint                       | Description                             |
|--------|--------------------------------|-----------------------------------------|
| POST   | `/api/patients/`               | Register new patient                    |
| POST   | `/api/doctors/`                | Register new doctor                     |
| POST   | `/api/appointments/`           | Create appointment                      |
| POST   | `/api/enqueue/`                | Add patient to doctor’s queue           |
| GET    | `/api/queue/<doctor_id>/`      | View current queue for a doctor         |
| POST   | `/api/notify-next/`            | Advance queue and notify next (admin)   |

---

## Admin Panel

- Accessible at: `http://localhost:8000/admin/`
- Manage:
  - Doctors and patients
  - Appointments
  - Queues
  - Notification logs

---
