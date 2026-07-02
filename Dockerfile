FROM python:3.11-slim

# Tell the cloud server to work inside its own main directory
WORKDIR /app

# Copy the requirements file from your folder straight into the cloud server
COPY requirements.txt .

# Install all the packages
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy everything else (app.py, logo.png, knowledge_base.txt) into the server
COPY . .

# Run your FastAPI app on Hugging Face's default port
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]