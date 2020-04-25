# second, we build the RTSP locator to locate exposed cameras
FROM python:3.7.7-slim-stretch
RUN mkdir /rtsp-locator
COPY ./requirements.txt /rtsp-locator/requirements.txt
RUN pip3 install -r /rtsp-locator/requirements.txt

COPY ./*.py /rtsp-locator/
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /rtsp-locator/wait-for

RUN apt-get update && apt-get install masscan gcc libglib2.0-0 -y