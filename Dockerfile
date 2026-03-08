# Use official Python runtime
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install all Python dependencies (LangChain, OpenAI, FastAPI, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend files specifically so the web server can serve them
COPY index.html .
COPY app.js .
COPY dashboard.js .
COPY index.css .
COPY dashboard.css .

# Copy the Python backend scripts (including server.py and LangChain files)
COPY *.py .

# Expose the port for Render to route traffic
EXPOSE 10000

# Start the FastAPI server (which serves the frontend AND connects to OpenAI)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10000"]
