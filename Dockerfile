FROM python:3.13-slim

WORKDIR /app

COPY frontend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]