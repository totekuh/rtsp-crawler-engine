#!/bin/bash

# add java repository
add-apt-repository ppa:webupd8team/java &&
apt update &&

apt install python3 python3-pip oracle-java8-installer maven mariadb-server tor mariadb-client &&
pip3 install requests flask opencv-python

# db initialization:
#CREATE DATABASE cameras_db;
#CREATE USER rtsp@localhost IDENTIFIED BY 'changeme3';
#GRANT ALL PRIVILEGES ON cameras_db.* TO rtsp@localhost IDENTIFIED BY 'changeme3';
