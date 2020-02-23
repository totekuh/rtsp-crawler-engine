#!/bin/bash

port=8080
host=localhost
database_name=cameras_db
database_user=rtsp
database_password=TGV0cyBmdWNrIHRpbGwgdGhlIHN1biBnb2VzIGRvd24K

cd ./rtsp-backend && mvn spring-boot:run -Dserver.port=$port -Dserver.address=$host -Dspring.datasource.username=$database_user -Dspring.datasource.password=$database_password -Dspring.datasource.url=jdbc:mariadb://localhost:3306/$database_name
