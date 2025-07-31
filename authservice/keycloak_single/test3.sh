

  curl -X POST \
    "http://keycloak:8080/realms/master/protocol/openid-connect/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "client_id=myclient&client_secret=9nv7PUBNyr3TB9FpwjO1gPbM2rDA0ELF&username=user01&password=bitnami1&grant_type=password&scope=openid groups"
