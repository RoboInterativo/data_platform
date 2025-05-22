#!/bin/bash

# Конфигурация
KEYCLOAK_HOST="localhost"
KEYCLOAK_PORT="8080"
REALM="master"
CLIENT_ID="myclient"
LOG_FILE="/var/log/keepalived_keycloak_check.log"

# Логирование
echo "$(date): Checking Keycloak availability for realm '$REALM' and client '$CLIENT_ID'..." >> $LOG_FILE

# Проверяем, запущен ли контейнер Keycloak
if ! docker ps --filter "name={{hostparam}}" {% raw %} --format "{{.Names}}" {% endraw %} | grep -q "keycloak"; then
    echo "$(date): Keycloak container is not running." >> $LOG_FILE
    exit 1
fi

# Проверяем доступность Keycloak через HTTP
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://${KEYCLOAK_HOST}:${KEYCLOAK_PORT}/realms/${REALM}/.well-known/openid-configuration)

if [ "$RESPONSE" -eq 200 ]; then
    echo "$(date): Keycloak is running and responding for realm '$REALM'." >> $LOG_FILE
    # exit 0
else
    echo "$(date): Keycloak is not responding for realm '$REALM'. HTTP response code: $RESPONSE" >> $LOG_FILE
    exit 1
fi

{% for item in services %}
nc -z localhost {{ services[item].port }} || exit 1
{% endfor %}
exit 0
