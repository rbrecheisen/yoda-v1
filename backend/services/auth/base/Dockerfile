FROM brecheisen/python-base:v1

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt
