TOKEN=$(curl -X POST \
  "http://127.0.0.1:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&client_id=myclient&client_secret=9nv7PUBNyr3TB9FpwjO1gPbM2rDA0ELF&username=admin&password=adminpassword&scope=openid" \
  | jq -r '.access_token'
)

echo "Токен: $TOKEN"

curl -s -X POST \
  "http://127.0.0.1:8080/realms/master/protocol/openid-connect/token/introspect" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Basic $(echo -n 'myclient:9nv7PUBNyr3TB9FpwjO1gPbM2rDA0ELF' | base64 -w0)" \
  -d "token=$TOKEN" | jq


  curl -v -X GET \
  "http://127.0.0.1:8080/realms/master/protocol/openid-connect/userinfo" \
  -H "Authorization: Bearer $TOKEN"

  curl -v \
     "http://127.0.0.1/api/ctrl/version" \
     -H "Authorization: Bearer $TOKEN"

echo test BAD TOKEN
curl -v    "http://127.0.0.1/api/ctrl/version"   -H "Authorization: Bearer BADTOKEN"
