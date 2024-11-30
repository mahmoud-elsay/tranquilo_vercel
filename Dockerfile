# Use a slim Python base image to minimize size
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to leverage Docker cache efficiently
COPY requirements.txt /app/

# Install dependencies in a virtual environment
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Set the PATH to use the virtual environment
ENV PATH="/venv/bin:$PATH"

# Copy the rest of the application files
COPY . /app/

# Expose the port Flask will run on
EXPOSE 5000

# Command to run your Flask app
CMD ["python", "app.py"]
