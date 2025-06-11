# Trust Evaluator Microservice

## Architecture and Technology
- **Language:** [Python](https://www.python.org/) 3.13+
- **API:** [FastAPI](https://fastapi.tiangolo.com/) (REST endpoints)
- **Trust Logic:** Custom trust computation and probabilistic evaluation
- **Dependency Management:** [Poetry](https://python-poetry.org/)
- **Containerization:** [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

## Overview
This microservice provides trust evaluation logic for the Trust Management System. It exposes REST endpoints for trust computation and interacts with the aggregator and frontend microservices.

## Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your system.

## Setup Instructions

### 1. Clone the Repository and Enter the Folder
```powershell
git clone https://github.com/Goncaslb/Trust-Evaluator-microservice
cd TrustEvaluatorMicroservice
```

### 2. Create the .env File
- Copy the contents of `.env.TEMPLATE` to a new file named `.env` in the same directory.

### 3. Create the Docker Network (only once)
Before running any microservice, create the shared Docker network (do this only once):
```powershell
# You only need to run this ONCE for all microservices
# You can do it in any of the microservice folders
# If the network already exists, Docker will not recreate it
docker network create trust_network
```

### 4. Start the Evaluator Microservice
From the `TrustEvaluatorMicroservice` directory, run:
```powershell
# Build and start the evaluator container
docker-compose up --build
```
This will build and start the evaluator container. By default, the API will be available at [http://localhost:8001](http://localhost:8001) (or the port specified in your `.env`).

### 5. Environment Variables
The `.env` file is already set up for Docker-based communication. No changes are needed unless you want to customize service names or ports.

## Notes
- Make sure the other microservices (TrustFrontend and TrustAggregator) are also running on the same `trust_network` for full functionality.
- If you change ports in the Docker or FastAPI config, update the port mapping in `docker-compose.yml` accordingly.
- For advanced testing or development, you can use Poetry to run the service locally (see comments in `main.py`).

---



