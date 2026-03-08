# Use official Python runtime
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install all Python dependencies (LangChain, OpenAI, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend files specifically so the web server can see them
COPY index.html .
COPY app.js .
COPY dashboard.js .
COPY index.css .
COPY dashboard.css .

# Copy the Python backend scripts too
COPY *.py .

# Expose the port for Render to route traffic
EXPOSE 10000

# Start a simple Python web server to serve the HTML Dashboard
# AND keep the container alive so you can run Python scripts in the Render Shell
CMD ["python", "-m", "http.server", "10000"]
