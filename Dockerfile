FROM python:3.11

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

COPY . /code/

