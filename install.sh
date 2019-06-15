#!/bin/bash

# add java repository
add-apt-repository ppa:webupd8team/java &&
apt update &&

apt install python3 python3-pip openjdk-8-jdk maven mariadb-server tor mariadb-client &&
pip3 install requests flask opencv-python

# db initialization:
#CREATE DATABASE cameras_db;
#CREATE USER rtsp@localhost IDENTIFIED BY 'changeme3';
#GRANT ALL PRIVILEGES ON cameras_db.* TO rtsp@localhost IDENTIFIED BY 'changeme3';

# configuring tor proxies to allow localhost:
# nano /etc/tor/torsocks.conf

# Set Torsocks to allow outbound connections to the loopback interface.
# If set to 1, connect() will be allowed to be used to the loopback interface
# bypassing Tor. This option should not be used by most users. (Default: 0)
#AllowOutboundLocalhost 1
