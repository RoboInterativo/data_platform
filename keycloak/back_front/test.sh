curl -v -X POST 'http://172.16.1.153/api/realms/master/protocol/openid-connect/token' \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=myclient&client_secret=9nv7PUBNyr3TB9FpwjO1gPbM2rDA0ELF&grant_type=password&username=admin&password=adminpassword&scope=openid"
#client_secret=echo -n 'myclient:rNEoR0SaH6ImZGEwfqEY4zVqocs58gMW' | base64

#9nv7PUBNyr3TB9FpwjO1gPbM2rDA0ELF
