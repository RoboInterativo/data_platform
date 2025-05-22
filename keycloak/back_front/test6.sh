
TOKEN=badtoken
curl -v \
"http://172.16.1.247/api/ctrl/version" \
-H "Authorization: Bearer $TOKEN"
