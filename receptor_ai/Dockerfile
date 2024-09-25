FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements.txt first and install the dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the FastAPI app to the container
COPY . /app

# Expose the FastAPI default port
EXPOSE 8000

# Command to run FastAPI using uvicorn, referencing main.py at root level
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]