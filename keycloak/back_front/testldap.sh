TOKEN=`curl -v -X POST \
  "http://172.16.1.153/api/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=admin-cli" \
  -d "client_secret=BHAGmIFXHKfHQFI2u2TXDyYn26LWqXjU" \
  -d "username=admin" \
  -d "password=adminpassword" \
  -d "grant_type=password" | jq .access_token`

echo $TOKEN


curl -X GET \
 "http://172.16.1.153/api/realms/master/components?parent=master&type=org.keycloak.storage.UserStorageProvider" \
 -H "Authorization: Bearer $TOKEN" \
 -H "Content-Type: application/json"
