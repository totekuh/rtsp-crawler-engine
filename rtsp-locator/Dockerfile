# second, we build the RTSP locator to locate exposed cameras
FROM python:3.7.7-slim-stretch
COPY . /rtsp-locator
WORKDIR /rtsp-locator
# install and cache required python dependencies
RUN pip3 install -r requirements.txt