FROM python:3.8

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update \
&& apt-get install -y binutils libproj-dev gdal-bin \
&& apt-get install -y vim vim-nox

RUN python -m venv /env \
&& /env/bin/pip install --upgrade pip \
&& /env/bin/pip install --no-cache-dir -r /tmp/requirements.txt

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ENV DJANGO_SETTINGS_MODULE=breakingbadapi_task.settings.dev

WORKDIR /app

COPY setup.py /app/
COPY src /app/src

COPY ./docker/django/start_local.sh /

RUN python setup.py develop
