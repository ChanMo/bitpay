FROM python:3.10-slim

RUN apt-get update && apt-get install -y cron
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN crontab task.cron

CMD ["gunicorn", "server.wsgi:application", "-w", "4", "-b", ":8000"]
