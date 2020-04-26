FROM python:3.7.7-slim-stretch
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /rtsp-neural-network/wait-for
RUN apt-get update \
&& apt-get install masscan gcc libglib2.0-0 libsm6 libxext6 libxrender-dev -y

COPY ./requirements.txt /rtsp-neural-network/requirements.txt
#COPY ./models /rtsp-neural-network/models
RUN pip3 install -r /rtsp-neural-network/requirements.txt


COPY ./rtsp-model.py /rtsp-neural-network/

# download a neural network model
RUN python3 -u /rtsp-neural-network/rtsp-model.py