# ApplyTrack API

A RESTful Job Application Tracker API built with **Python**, **FastAPI**, **SQLAlchemy**, **PostgreSQL (Neon)**, and **Docker**.

ApplyTrack API is a RESTful backend application for tracking job applications, built with Python, FastAPI, SQLAlchemy, and PostgreSQL. The project demonstrates practical backend engineering skills including REST API design, request validation, database persistence, automated testing, containerization with Docker, and cloud-ready application architecture.

---

## Features

- RESTful CRUD API for managing job applications
- Request validation with Pydantic
- PostgreSQL database hosted on Neon
- SQLAlchemy ORM
- Automated API testing with pytest
- Dockerized application
- Interactive API documentation with Swagger UI

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| FastAPI | Backend Framework |
| SQLAlchemy | ORM |
| PostgreSQL (Neon) | Database |
| Pydantic | Data Validation |
| Pytest | Testing |
| Uvicorn | ASGI Server |
| Docker | Containerization |

---

## Project Structure

```text
applytrack-api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── config.py
│
├── tests/
│
├── Dockerfile
├── .dockerignore
├── pytest.ini
├── requirements.txt
├── .env.example
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| GET | `/applications` | Retrieve all applications |
| GET | `/applications/{id}` | Retrieve a single application |
| POST | `/applications` | Create an application |
| PUT | `/applications/{id}` | Update an application |
| DELETE | `/applications/{id}` | Delete an application |

---

## Running Locally

### Clone the repository

```bash
git clone <repository-url>
cd applytrack-api
```

### Create a virtual environment

```bash
python -m venv venv
```

macOS / Linux

```bash
source venv/bin/activate
```

Windows

```powershell
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=your_neon_connection_string
```

### Run the application

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://localhost:8000/docs
```

---

## Running Tests

```bash
pytest
```

Current test coverage includes:

- Root endpoint
- Health endpoint
- Create application
- Retrieve applications
- Retrieve application by ID
- Update application
- Delete application

---

## Docker

Build the Docker image:

```bash
docker build -t applytrack-api .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 applytrack-api
```

Open:

```
http://localhost:8000/docs
```

---

## Key Concepts Demonstrated

- REST API design
- FastAPI project organization
- Request validation with Pydantic
- SQLAlchemy ORM
- PostgreSQL integration
- Dependency Injection
- CRUD operations
- Automated API testing with pytest
- Docker containerization
- Cloud-ready application architecture

---

## Author

**Gerard Eklu**