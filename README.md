# URL Monitor App

This is a simple web application built with FastAPI to monitor the status of URLs provided by users. The app checks the status of the URLs and stores them in a PostgreSQL database for tracking purposes. It uses Docker for containerization, making it easy to deploy and manage.

## Features

- Users can enter a URL to check its status.
- Displays whether the URL is "OK" (status 200) or returns an error status code.
- Stores checked URLs and their statuses in a PostgreSQL database.
- Docker and Docker Compose setup for easy deployment.

## Prerequisites

Make sure you have the following installed:

- Docker
- Docker Compose

## Setup

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/url-monitor.git
cd url-monitor
```
### 2. Build and run the application using Docker Compose:
```bash
docker-compose up --build
```

This command will build the Docker images and start the application along with a PostgreSQL database. The FastAPI app will be accessible on http://localhost:8000.

### 3. Access the application:
Once the containers are running, you can visit the application in your browser at http://localhost:8000.

### 4. Monitor URL Status:
Enter any URL into the input box and click "Check Status."
The application will show the status of the URL (either "OK" or an error message with the corresponding status code).
The URLs and their statuses will be stored in the PostgreSQL database.

## Project Structure

<img width="623" alt="Screenshot 2025-05-12 at 14 35 08" src="https://github.com/user-attachments/assets/3328e794-0af6-447a-beaf-c196243fffd3" />

## Docker Configuration

The project uses Docker to containerize the FastAPI application and PostgreSQL database. The Dockerfile defines how the app container is built, and docker-compose.yml orchestrates the services.

### Docker Compose
The docker-compose.yml file defines two services:

web: The FastAPI app that runs on port 8000.
db: The PostgreSQL database where the URL statuses are stored.

### Dockerfile
The Dockerfile is used to build the image for the FastAPI application. It starts from a Python 3.11 image, installs dependencies, and runs the FastAPI app using uvicorn.

## Database

The app uses PostgreSQL to store the URLs and their statuses. The database.py file handles the database connection, and the urls table keeps track of the following:

id: Primary key, auto-incremented.
url: The URL that was checked.
status: The status of the URL (e.g., "OK" or an error message).

## Testing

Tests can be added in the future to verify that the URL monitoring functionality works as expected. For now, you can manually test the app by interacting with the form.

## CI/CD with GitHub Actions

This project includes a basic GitHub Actions setup for Continuous Integration and Continuous Deployment (CI/CD). Every push to the repository will trigger a workflow that:

Builds the Docker image.
Runs any tests (if added in the future).
Deploys the app.
