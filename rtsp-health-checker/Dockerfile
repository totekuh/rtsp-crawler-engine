# third, we build a health-checker for the exposed cameras
FROM python:3.7.7-slim-stretch
RUN mkdir /rtsp-health-check
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /rtsp-health-check/wait-for
RUN apt-get update \
&& apt-get install masscan gcc libglib2.0-0 libsm6 libxext6 libxrender-dev -y

COPY requirements.txt /rtsp-health-check
RUN pip3 install -r /rtsp-health-check/requirements.txt

COPY rtsp-health-checker.py /rtsp-health-check

