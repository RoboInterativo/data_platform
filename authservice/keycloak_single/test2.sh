# Получите токен администратора
ADMIN_TOKEN=$(curl -s -X POST \
  "http://keycloak:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_secret=BHAGmIFXHKfHQFI2u2TXDyYn26LWqXjU&client_id=admin-cli&username=admin&password=adminpassword&grant_type=password" | jq -r '.access_token')

# Проверьте доступные scopes для myclient
curl -s -X GET \
  "http://keycloak:8080/admin/realms/master/clients/$(curl -s -X GET "http://keycloak:8080/admin/realms/master/clients?clientId=myclient" -H "Authorization: Bearer $ADMIN_TOKEN" | jq -r '.[0].id')" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq
  # '.defaultClientScopes'
