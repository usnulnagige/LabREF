FROM maven:3.8.5-openjdk-17-slim AS build

WORKDIR /app

COPY pom.xml /app/
COPY src/ /app/src/

RUN mvn clean package -DskipTests


FROM eclipse-temurin:17.0.14_7-jre-jammy

WORKDIR /app

COPY --from=build /app/target/*.jar /app/app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
