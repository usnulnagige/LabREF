FROM maven:3.8.5-openjdk-17-slim AS builder

WORKDIR /app

COPY pom.xml /app/
COPY src/ /app/src/

RUN mvn clean package -DskipTests

FROM openjdk:17-slim

WORKDIR /app

COPY --from=builder /app/target/*.jar /app/app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]