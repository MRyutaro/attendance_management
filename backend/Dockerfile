FROM python:3.11.2

WORKDIR /backend

COPY . .

RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py createsuperuser --noinput