FROM python:3.7.7-slim-stretch
RUN mkdir /rtsp-neural-network
COPY ./requirements.txt /rtsp-neural-network/requirements.txt
RUN pip3 install -r /rtsp-neural-network/requirements.txt


ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /rtsp-neural-network/wait-for
COPY ./rtsp-model.py /rtsp-neural-network/