# healthcare-queue-management

---

```markdown
# Healthcare Appointment and Queue Management System

A full-stack web application to streamline patient appointment scheduling, real-time queue management, and automated notifications for clinics and hospitals.

## Features

- Patient registration and doctor selection
- Appointment scheduling with queue management
- Real-time queue updates via WebSockets
- JWT-based user authentication (patients, doctors, admins)
- SMS notifications (Twilio) for patient turn alerts
- Notification logging and admin management panel
- RESTful API built with Django REST Framework
- Containerized with Docker and orchestrated using Docker Compose

---

## Tech Stack

### Backend
- Django (REST Framework)
- PostgreSQL
- Celery (Task Queue)
- Redis (Broker for Celery and WebSockets)
- Django Channels (WebSocket support)
- Simple JWT (Authentication)
- Twilio (SMS notifications)

### Frontend (Optional)
- React (Patient/Admin dashboard UI)

---

## Project Structure

```
healthcare-queue-management/
├── backend/              # Django Backend (REST APIs, WebSockets)
│   ├── appointments/     # App logic: models, views, serializers, tasks
│   ├── healthcare/       # Project settings, routing, ASGI/WSGI setup
│   ├── manage.py
│   ├── requirements.txt
├── frontend/             # React Frontend (optional)
├── docker-compose.yml
└── README.md
```

---

## Authentication

- Uses JWT tokens (via SimpleJWT) for secure login
- Admins/staff are required to perform queue actions like notify-next
- Token Endpoints:
  - `POST /api/token/` (obtain token)
  - `POST /api/token/refresh/` (refresh token)

---

## Real-Time Queue Updates

- WebSocket endpoint:  
  `ws://localhost:8000/ws/queue/<doctor_id>/`

- Clients subscribed to this channel receive real-time queue updates when a change occurs.

---

## Notifications

- SMS notifications are sent using Twilio
- Notifications are logged to the database
- When a patient reaches the front of the queue, they receive a message like:  
  `"It is your turn. Please proceed to the doctor's office."`

---

## Getting Started (with Docker)

### Prerequisites

- Docker and Docker Compose installed on your machine

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/healthcare-queue-management.git
cd healthcare-queue-management
```

### 2. (Optional) Set Environment Variables

You can define Twilio credentials as environment variables, or edit directly in `settings.py`.

```bash
export TWILIO_ACCOUNT_SID=your_account_sid
export TWILIO_AUTH_TOKEN=your_auth_token
export TWILIO_FROM_NUMBER=+1234567890
```

### 3. Build Docker Containers

```bash
docker-compose build
```

### 4. Start All Services

```bash
docker-compose up
```

### 5. Create a Superuser for Admin Panel

```bash
docker-compose exec backend python manage.py createsuperuser
```

Then visit `http://localhost:8000/admin/` to log in.

---

## API Endpoints

| Method | Endpoint                          | Description                            |
|--------|-----------------------------------|----------------------------------------|
| POST   | `/api/patients/`                  | Create a patient                       |
| POST   | `/api/doctors/`                   | Create a doctor                        |
| POST   | `/api/appointments/`              | Create an appointment                  |
| POST   | `/api/enqueue/`                   | Add patient to queue                   |
| GET    | `/api/queue/<doctor_id>/`         | Get current queue for a doctor         |
| POST   | `/api/notify-next/`               | Notify and advance queue (admin only)  |
| POST   | `/api/token/`                     | Obtain JWT token                       |
| POST   | `/api/token/refresh/`             | Refresh JWT token                      |

---

## Admin Dashboard

- Accessible at: `http://localhost:8000/admin/`
- Manage doctors, patients, appointments, and view notification logs

---

## Future Enhancements

- Doctor availability and time slot scheduling
- Patient self-check-in via mobile web app
- Email notification support
- Analytics dashboard and reporting

---

## License

MIT License  
Copyright (c) 2025

---

## Screenshots / Diagrams (Optional)

Add UI wireframes, system diagrams, or live screenshots here to help users understand how the system looks and works.

```
