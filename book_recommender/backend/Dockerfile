FROM python:3.12-slim

WORKDIR /backend

COPY models ./models
COPY routers ./routers
COPY __init__.py .
COPY dependencies.py .
COPY main.py .
COPY requirements.txt .
COPY .env .

RUN apt update && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["fastapi", "run", "main.py"]