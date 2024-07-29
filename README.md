# Event Management

This project represents event management, featuring integration with Celery for asynchronous task processing along with Redis for caching.

## Setup Instructions

### Prerequisites

- Python 3.x installed on your system.
- Redis server installed and running locally.
- RabbitMQ server installed and running locally (required for Celery).

### Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/harshitNinjatech/event.git
   cd event
   ```

2. **Create and activate a virtual environment using `pipenv`:**
   ```
   pipenv install --dev
   pipenv shell
   ```
   This will create and activate a virtual environment (`venv`) and install all dependencies, including development ones.

3. **Set up environment variables:**
   - Copy the `.env.dev.example` file and rename it to `.env.dev`.
   - Update the `.env.dev` file with your local development settings.

4. **Apply initial database migrations:**
   ```
   python manage.py migrate
   ```

### Running the Server

1. **Start the Django development server:**
   ```
   python manage.py runserver
   ```

2. **Access the API documentation:**
   - Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
   - ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

### Managing Celery Tasks

1. **Start a Celery worker for processing tasks:**
   ```
   celery -A event worker --loglevel=info
   ```

2. **Start Celery Beat for scheduling periodic tasks (optional):**
   ```
   celery -A event beat --loglevel=info
   ```

3. **Manually fetch events using Management command & Celery task (optional):**
   ```
   python manage.py fetch_save_event"
   ```

### API Endpoints

- **List Events:** [http://localhost:8000/api/events-list/](http://localhost:8000/api/events-list/)
  - **Parameters:** `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD)
  - **Description:** Retrieve events filtered by start and end dates.

## Environment Files

- **Development Environment:** `.env.dev`
  - Use this file for local development settings. Copy `.env.dev.example` and remove `.example` to configure.

- **Production Environment:** `.env.prod`
  - Use this file for production settings. Copy `.env.prod.example` and remove `.example` to configure.

## Pre-commit Hooks

To install and set up `pre-commit` hooks for code formatting and linting:

1. **Install `pre-commit`:**
   ```
   pipenv install --dev
   ```

2. **Set up `pre-commit`:**
   ```
   pipenv run pre-commit install
   ```
   This will install `pre-commit` and set up hooks to run before each commit, ensuring code quality and style checks.

---
