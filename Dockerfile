FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
ENV SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@host.docker.internal:5432/firmware_analyzer

EXPOSE 8080

CMD ["python", "app.py"]