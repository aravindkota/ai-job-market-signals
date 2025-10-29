# PURPOSE: Containerize the service for local/dev/prod environments.
# - Installs dependencies
# - Exposes FastAPI app on port 8000 (adjust as needed)

FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# For local dev you might use: uvicorn app.api.main:app --host 0.0.0.0 --port 8000
EXPOSE 8000

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
