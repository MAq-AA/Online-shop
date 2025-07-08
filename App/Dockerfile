FROM python:3.12.2

COPY images/* /images/
ADD . /opt/Django-app
WORKDIR /opt/Django-app

RUN pip install Django
RUN pip install psycopg2
RUN pip install Pillow
RUN pip install django-filter
RUN pip install Django_phonenumber_field
RUN pip install phonenumbers
RUN pip install whitenoise

EXPOSE 5000

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
