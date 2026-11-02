markdown
# Enterprise FinTech Traffic Generator

A high-performance, asynchronous microservice designed to simulate large-scale transaction streams and system logs for financial platforms (similar to Allegro Pay ecosystem). Built with **Python 3.11**, **FastAPI**, and **Pydantic**, the system features a web-based DevOps Control Panel and is fully containerized using **Docker**.

## 🚀 Key Features

* **Asynchronous Architecture:** Leverages Python's `asyncio` and FastAPI `BackgroundTasks` to generate high-volume data streams concurrently without blocking the web server.
* **Enterprise Data Validation:** Utilizes **Pydantic v2** models to enforce strict schema compliance and runtime data validation (UUID generations, ISO timestamps).
* **Fraud & Anomaly Injection:** Simulates realistic user behavior combined with a probabilistic anomaly engine (5% chance to inject high-value fraudulent transaction patterns with `SUSPICIOUS` flags).
* **DevOps Control Panel:** Lightweight, responsive HTML/CSS dashboard built directly into the microservice to start, stop, and monitor the stream in real-time.
* **Production-Ready Containerization:** Standardized environments utilizing multi-stage Docker configurations to ensure seamless deployment to any cloud provider.

## 🛠️ Tech Stack

* **Language:** Python 3.11 (Slim production image)
* **Framework:** FastAPI
* **Data Validation:** Pydantic v2
* **Data Simulation:** Faker
* **Server:** Uvicorn (ASGI)
* **DevOps:** Docker & Docker Compose

## 📦 Local Installation & Deployment

To spin up the entire infrastructure locally, ensure you have **Docker** and **Docker Compose** installed, then execute:

```bash
docker-compose up --build
```

Once the build is complete, open your browser and navigate to:
👉 **http://localhost:8000**

## 🌐 System Architecture

```mermaid
graph TD
    User[Recruiter / Browser] -->|HTTP GET /| FastAPI[FastAPI Web Server]
    User -->|POST /start| FastAPI
    FastAPI -->|Spawns Background Task| Loop[Asynchronous Traffic Loop]
    Loop -->|Generates Mock Data| Faker[Faker & Pydantic Validator]
    Faker -->|Injects 5% Fraud Anomalies| Stream[Structured JSON Log Stream]
    Stream -->|Outputs| Console[Stdout / Docker Logs]
