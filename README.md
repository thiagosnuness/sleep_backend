
# SleepCheck - Backend

This is the backend of the **SleepCheck** application, developed as part of the **Software Engineering** course at **PUC Rio**. The backend is responsible for processing user input, generating predictions for sleep disorders using a trained machine learning model, and managing these records in a database.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [License](#license)
- [Contact](#contact)

## Overview

SleepCheck is a health-oriented application designed to help users evaluate potential sleep disorders. The backend handles the logic of data input, runs predictions based on a trained model, and exposes a RESTful API for integration with the frontend.

## Features

- **Machine Learning Integration**: Predicts potential sleep disorders based on health and lifestyle data.
- **RESTful API**: Built with Flask and documented using Swagger.
- **SQLite Database**: Stores all prediction records.
- **Endpoints**:
  - `POST /predict`: Submit new data and receive prediction
  - `GET /records`: Retrieve all past predictions
  - `DELETE /prediction?id=X`: Delete a prediction by ID
- **Swagger UI**: Available at `/openapi` for easy exploration of all endpoints.

## Technologies

- **Python 3.x**
- **Flask**
- **Flask-SQLAlchemy**
- **Flask-OpenAPI3**
- **SQLite**
- **Docker / Docker Compose**
- **Pytest** (for automated tests)

## Installation

### Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Run the full application (frontend + backend)

1. **Clone the repositories**:

   ```bash
   git clone https://github.com/thiagosnuness/sleep_frontend.git
   git clone https://github.com/thiagosnuness/sleep_backend.git
   ```

2. **Navigate to the frontend folder** (where the `docker-compose.yml` is located):

   ```bash
   cd sleep_frontend
   ```

3. **Run everything with Docker Compose**:

   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend: [http://localhost](http://localhost)
   - Backend API (Swagger): [http://localhost:5000/openapi](http://localhost:5000/openapi)

### Run the backend standalone

If you want to run just the backend:

```bash
cd sleep_backend
docker build -t sleep_backend .
docker run -d -p 5000:5000 --name sleep_backend sleep_backend
```

Then open [http://localhost:5000/openapi](http://localhost:5000/openapi)

## Running Tests

The backend includes automated tests using `pytest`.

If your application is running via Docker Compose, you can execute the tests without stopping the main containers:

```bash
cd sleep_frontend
docker compose run --rm sleep_backend_test
```

> This runs the tests inside an isolated container, based on the same backend image, using the test configuration.

Alternatively, if you're inside the backend container:

```bash
cd sleep_backend
docker exec -it sleep_backend pytest -v tests/test_api.py
```

## License

This project is licensed under the **MIT License**.

## Contact

For any questions, feedback, or suggestions, feel free to reach out:

- **Thiago Nunes** - [GitHub Profile](https://github.com/thiagosnuness)
- **SleepCheck Backend**: [https://github.com/thiagosnuness/sleep_backend](https://github.com/thiagosnuness/sleep_backend)
- **SleepCheck Frontend**: [https://github.com/thiagosnuness/sleep_frontend](https://github.com/thiagosnuness/sleep_frontend)
