curl -X POST 'http://localhost/api/realms/master/protocol/openid-connect/token' \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=myclient&client_secret=rNEoR0SaH6ImZGEwfqEY4zVqocs58gMW&grant_type=password&username=admin&password=adminpassword"
client_secret=echo -n 'myclient:rNEoR0SaH6ImZGEwfqEY4zVqocs58gMW' | base64

9nv7PUBNyr3TB9FpwjO1gPbM2rDA0ELF
