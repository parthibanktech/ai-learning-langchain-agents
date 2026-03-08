# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy just the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Python code into the container
COPY . .

# (Optional) Since this is a learning lab with multiple scripts and a separate front-end,
# we default to running the "Masterpiece" mini-project when the container starts.
CMD ["python", "09_mini_project_research_assistant.py"]
