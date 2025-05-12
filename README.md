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
