# -- Base Python Image --
FROM python:3.11-slim

# ---- Environment Variables ----
# POETRY_VERSION: pins the version of Poetry to 2.1.3 for consistent builds.
# PYTHONDONTWRITEBYTECODE=1: disables .pyc files (no __pycache__).
# PYTHONUNBUFFERED=1: disables Python stdout/stderr buffering so logs show up instantly (crucial in Docker).
ENV POETRY_VERSION=2.1.3 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---- System Dependencies ----
# Installs build tools and curl.
# Installs Poetry (v2.1.3) via the official installer.
# Symlinks it to /usr/local/bin/poetry so it’s globally accessible.
# Cleans up unneeded packages to reduce image size.
RUN apt-get update && apt-get install -y curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get purge -y curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# ---- Set Work Directory ----
#Sets the default working directory inside the container to /app.
#All future commands (like COPY, RUN, CMD) are executed from here.
WORKDIR /app

# ---- Copy and Install Dependencies ----
#Copies dependency descriptors (pyproject.toml and poetry.lock) first to leverage Docker layer caching.
#Installs dependencies system-wide (no virtualenv).
#--no-interaction --no-ansi: makes it suitable for automated/scripted installs.
COPY pyproject.toml poetry.lock* README.md ./
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi


# ---- Copy App Code ----
#Copies the rest of your application code into /app.
# after copy
# /app/
# ├── backend/
# ├── pyproject.toml
# ├── README.md
# ├── .env

COPY . .

# ---- Expose App Port ----
#Tells Docker that this container listens on port 8000.
# Informational only; actual port mapping is done during docker run -p.
EXPOSE 8080

# ---- Start FastAPI App with Gunicorn + Uvicorn Worker ----
#Runs the FastAPI app using:
#Gunicorn as a process manager
#UvicornWorker for handling asynchronous requests
CMD ["gunicorn", "backend.app:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "--workers", "4"]