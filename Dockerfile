FROM python:3.9

WORKDIR /source

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements/production.txt /source/
COPY requirements/base.txt /source/
COPY requirements/dev.txt /source/

RUN apt-get update && apt-get install -y build-essential libpq-dev
RUN pip install --upgrade pip && pip install -r production.txt

COPY . /source/

CMD ["gunicorn", "project.wsgi", ":8000"]