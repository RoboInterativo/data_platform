
TOKEN=badtoken
curl -v \
"http://127.0.0.1/api/ctrl/version" \
-H "Authorization: Bearer $TOKEN"
