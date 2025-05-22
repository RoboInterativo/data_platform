FROM python:3.12
EXPOSE 8000
ENV HOME=/opt/app
WORKDIR /opt/app

COPY src/requirements.txt /tmp/requirements.txt
COPY src .


RUN pip install virtualenv  &&\
    python -m virtualenv /opt/venv &&\
    chown 1001:1001 /opt/ -R

USER 1001

RUN . /opt/venv/bin/activate &&\
    pip install pip --upgrade &&\
    pip install -r  /tmp/requirements.txt &&\
    cd /opt/app/ && ls -li


CMD . /opt/venv/bin/activate && cd /opt/app/ && uwsgi --http 0.0.0.0:5555 --module main --callable app
