FROM maven:3.9-eclipse-temurin-17-alpine AS build
WORKDIR /app
COPY keycloak-users-with-groups .
RUN mvn clean package -DskipTests

FROM bitnami/keycloak:26.2.5
USER root
COPY --from=build /app/target/keycloak-users-with-groups-1.0.0.jar /opt/bitnami/keycloak/providers/
RUN chmod 644 /opt/bitnami/keycloak/providers/keycloak-users-with-groups-1.0.0.jar && \
    chown 1001:root /opt/bitnami/keycloak/providers/keycloak-users-with-groups-1.0.0.jar
USER 1001
# # Собираем Keycloak с плагином (обязательно!)
RUN  /opt/bitnami/keycloak/bin/kc.sh build &&\
 /opt/bitnami/keycloak/bin/kc.sh show-config
