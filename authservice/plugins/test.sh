TOKEN=$(curl -X POST \
  "http://127.0.0.1:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=admin-cli&grant_type=password&username=admin&password=adminpassword&scope=openid" \
  | jq -r '.access_token'
)
echo "TOKEN $TOKEN"

# curl -v -X GET \
#   "http://127.0.0.1:8080/realms/master/protocol/openid-connect/userinfo" \
#   -H "Authorization: Bearer $TOKEN"


  curl -X GET \
    -H "Authorization: Bearer $TOKEN" \
    "http://localhost:8080/admin/realms/master/users" |jq

curl -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8080/admin/realms/master/users-with-groups" |jq
