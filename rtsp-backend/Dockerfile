# first, we build the backend API
FROM maven:3.6.3-jdk-8-slim AS MAVEN_BUILD
COPY pom.xml /build/
WORKDIR /build/
# build all dependencies for offline use
RUN mvn dependency:go-offline -B
# copy your other files
COPY src /build/src/
# build for release
RUN  mvn clean package -DskipTests

FROM openjdk:8-jdk-slim
RUN mkdir /rtsp-backend
COPY --from=MAVEN_BUILD /build/target/cameras*.jar /rtsp-backend/cameras.jar
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /rtsp-backend/wait-for