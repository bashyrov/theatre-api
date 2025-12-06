# Theatre API

**Online theatre ticket booking service**  
Modern REST API built with **Django REST Framework**, featuring JWT authentication, interactive documentation, and full online ticket booking functionality.

[![Django](https://img.shields.io/badge/Django-5.2%2B-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16%2B-A30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![DRF Spectacular](https://img.shields.io/badge/DRF_Spectacular-0.29-6C4AB6?style=for-the-badge&logo=swagger&logoColor=white)](https://drf-spectacular.readthedocs.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## Features

- User registration & login via **JWT**
- Browse plays, actors, genres, and theatre halls
- Online ticket booking with seat selection
- Manage personal reservations
- Full OpenAPI documentation (Swagger + ReDoc)

---

### Authentication (JWT)

| Endpoint            | Method   | Description                              |
|---------------------|----------|------------------------------------------|
| `/register/`        | POST     | Register a new user                      |
| `/token/`           | POST     | Obtain access & refresh tokens           |
| `/token/refresh/`   | POST     | Refresh access token                     |
| `/token/verify/`    | POST     | Verify token validity                    |
| `/me/`              | GET/PUT  | View and update current user profile     |

### Main API Endpoints

| Endpoint             | Methods                  | Description                                      |
|----------------------|--------------------------|--------------------------------------------------|
| `/theatre-halls/`    | GET, POST, PUT, DELETE   | Theatre halls (create, list, update, delete)     |
| `/actors/`           | GET, POST, PUT, DELETE   | Actors (create, list, update, delete)            |
| `/genres/`           | GET, POST, PUT, DELETE   | Play genres (create, list, update, delete)       |
| `/plays/`            | GET, POST, PUT, DELETE   | Plays (create, list, update, delete)             |
| `/performances/`     | GET, POST, PUT, DELETE   | Showtimes (date, time, hall)                     |
| `/tickets/`          | GET, POST, PUT, DELETE   | Tickets — **requires authentication**            |
| `/reservations/`     | GET, POST, PUT, DELETE   | Reservations — **requires authentication**       |

> Protected endpoints require header:  
> `Authorization: Bearer <access_token>`

---

## Quick Start

## Option 1: Docker (Recommended)

```bash
git clone https://github.com/bashyrov/theatre-api.git
cd theatre-api
docker-compose up --build
```
### Load sample data

```bash
docker-compose exec theatre_app sh
python manage.py loaddata theatre_fixture_en.json
```

API will be available at: http://127.0.0.1:8001

## Option 2: Local Development
```bash
git clone https://github.com/bashyrov/theatre-api.git
cd theatre-api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```
### Create .env file (or copy from .env_sample):

```bash
DJANGO_SECRET_KEY=your_very_secret_key_here
DJANGO_DEBUG=True
POSTGRES_DB=theatre_db
POSTGRES_USER=theatre_user
POSTGRES_PASSWORD=theatre_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Start PostgreSQL via Docker:

```bash
docker run --name theatre-postgres \
  -e POSTGRES_DB=theatre_db \
  -e POSTGRES_USER=theatre_user \
  -e POSTGRES_PASSWORD=theatre_pass \
  -p 5432:5432 -d postgres
```

### Apply migrations and load sample data:

```bash
python manage.py migrate
python manage.py loaddata theatre_fixture_en.json
python manage.py runserver
```

### Registration example:

```bash
POST users/register/
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

### Test Admin Account

```bash
Email: admin@admin.com
Password: S7/J=a}2`C5$
```

## 📚 API Documentation
Interactive documentation available after server start:

Swagger UI: http://127.0.0.1:8001/api/schema/swagger-ui/

ReDoc: http://127.0.0.1:8001/api/schema/redoc/


OpenAPI Schema: http://127.0.0.1:8001/api/schema/


