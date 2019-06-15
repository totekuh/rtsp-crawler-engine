#!/bin/bash

port=80
host=localhost

cd ./java && mvn spring-boot:run -Dserver.port=$port -Dserver.address=$host
