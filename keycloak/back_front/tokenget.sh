# curl -v -X POST \
#   "http://127.0.0.1/api/realms/master/protocol/openid-connect/token" \
#   -H "Content-Type: application/x-www-form-urlencoded" \
#   -d "grant_type=password&client_id=myclient&client_secret=9nv7PUBNyr3TB9FpwjO1gPbM2rDA0ELF&username=admin&password=adminpassword&scope=openid+profile+email" \
#   | jq

URL=http://172.16.1.247
curl -X POST \
  "$URL/api/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=myclient&client_secret=9nv7PUBNyr3TB9FpwjO1gPbM2rDA0ELF&username=user01&password=bitnami1&grant_type=password&scope=openid groups"  | jq -r '.access_token'


URL=http://172.16.1.247
curl -X POST \
  "$URL:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=myclient&client_secret=9nv7PUBNyr3TB9FpwjO1gPbM2rDA0ELF&username=user01&password=bitnami1&grant_type=password&scope=openid groups"  | jq -r '.access_token'
