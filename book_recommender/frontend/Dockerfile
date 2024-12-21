FROM python:3.12-slim

WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN apt update && pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py"]