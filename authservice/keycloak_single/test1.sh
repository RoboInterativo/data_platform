curl -X POST \
  "http://keycloak:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=admin-cli&client_secret=BHAGmIFXHKfHQFI2u2TXDyYn26LWqXjU&username=user01&password=bitnami1&grant_type=password"
