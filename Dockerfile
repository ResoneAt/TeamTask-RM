FROM python:3.9

WORKDIR /source

COPY requirements/production.txt /source/
COPY requirements/base.txt /source/
COPY requirements/dev.txt /source/


RUN pip install --upgrade pip
RUN pip install -r production.txt

COPY . /source/

CMD ["gunicorn", "project.wsgi", ":8000"]