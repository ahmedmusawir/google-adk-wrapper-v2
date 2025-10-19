# Step 1: Use a modern, lightweight Python base image.
FROM python:3.12-slim

# Step 2: Set the working directory inside the container.
WORKDIR /app

# Step 3: Copy the dependencies file and install the required packages.
# This is done first to leverage Docker's layer caching for faster rebuilds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy all your application files (main.py, config.py, config.json) into the container.
COPY . .

# Step 5: Set the environment to "cloud".
# This tells your config.py to use the live Cloud Run URL for the ADK Bundle.
ENV APP_ENV="cloud"

# Step 6: Define the command to start the FastAPI server.
# It listens on all network interfaces (--host 0.0.0.0) and uses the port
# number provided by the Cloud Run environment (${PORT}).
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}