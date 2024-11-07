###
openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days 365 -CAcreateserial -passin pass:12345678

keytool -keystore kafka.client.keystore.jks -alias CARoot -import -file ca-cert

keytool -keystore kafka.client.keystore.jks -alias localhost -import -file cert-signed
