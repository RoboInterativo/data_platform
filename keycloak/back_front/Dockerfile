FROM openresty/openresty:alpine

# Копируем конфиги
COPY nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
# COPY lua_scripts /usr/local/openresty/lualib/

# Указываем переменные по умолчанию (опционально)
# ENV KEYCLOAK_CLIENT_ID="default_client" \
#     KEYCLOAK_CLIENT_SECRET="default_secret" \
#     KEYCLOAK_REALM="master" \
#     KEYCLOAK_URL="http://keycloak:8080"
