# Stage 1: Build dependencies
FROM python:3.9-alpine as builder

WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies in a virtual environment and clean up
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip  # Clean up pip cache to reduce image size

# Stage 2: Final image with only necessary files
FROM python:3.9-alpine

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

# Copy only necessary project files (omit unnecessary files like test files, logs, etc.)
COPY . /app/

# Set environment variable for virtual environment
ENV PATH="/venv/bin:$PATH"

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
