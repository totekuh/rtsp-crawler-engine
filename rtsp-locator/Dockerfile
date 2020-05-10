# second, we build the RTSP locator to locate exposed cameras
FROM python:3.7.7-slim-stretch
RUN mkdir /rtsp-locator
COPY ./requirements.txt /rtsp-locator/requirements.txt
RUN pip3 install -r /rtsp-locator/requirements.txt
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /rtsp-locator/wait-for
RUN apt-get update \
&& pip3 install https://github.com/mitsuhiko/click/tarball/master \
&& easy_install shodan \
&& apt-get install masscan gcc libglib2.0-0 libsm6 libxext6 libxrender-dev gzip -y

COPY ./*.py /rtsp-locator/
WORKDIR /rtsp-locator
ENTRYPOINT if [ "x$SHODAN_API_KEY" = "x" ] ; then /bin/bash wait-for rtsp-backend:8080 -t 0 \
                                           -- python3 -u /rtsp-locator/rtsp-spyglass.py --country-code $COUNTRY_CODE \
                                           --import-endpoint http://rtsp-backend:8080/cameras/import ; \
                                           else /bin/bash wait-for rtsp-backend:8080 -t 0 \
                                                -- python3 -u /rtsp-locator/rtsp-spyglass.py --country-code $COUNTRY_CODE \
                                                --import-endpoint http://rtsp-backend:8080/cameras/import \
                                                --shodan-api-key $SHODAN_API_KEY; \
                                           fi