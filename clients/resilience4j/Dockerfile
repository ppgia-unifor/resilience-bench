FROM maven:3.8.3-openjdk-11-slim AS build
COPY src /usr/src/app/src
COPY pom.xml /usr/src/app
RUN mvn -f /usr/src/app/pom.xml clean package

FROM openjdk:11
COPY --from=build /usr/src/app/target/resilience4j-0.0.1-SNAPSHOT.jar /usr/app/resilience4j-0.0.1-SNAPSHOT.jar
EXPOSE 80
ENTRYPOINT ["java","-jar","/usr/app/resilience4j-0.0.1-SNAPSHOT.jar"]