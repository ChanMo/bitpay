FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["gunicorn", "service.wsgi:application", "-w", "4", "-b", "8000"]
