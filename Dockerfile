FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]