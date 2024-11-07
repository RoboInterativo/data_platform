#https://help.hcl-software.com/unica/Journey/en/12.1.0/Journey/AdminGuide/Configuration_of_kafka_on_SSL.html
keytool -keystore kafka.server.keystore.jks -alias localhost -validity 365 -genkey

openssl req -new -x509 -keyout ca-key -out ca-cert -days 365
keytool -keystore kafka.server.truststore.jks -alias CARoot -import -file ca-cert
keytool -keystore kafka.client.truststore.jks -alias CARoot -import -file ca-cert
keytool -keystore kafka.server.keystore.jks -alias localhost -certreq -file cert-file
openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days 365 -CAcreateserial -passin pass:12345678
keytool -keystore kafka.server.keystore.jks -alias CARoot -import -file ca-cert

keytool -keystore kafka.server.keystore.jks -alias localhost -import -file cert-signed
#Create client keystore and import both certificates of the CA and signed certificates to client keystore. These client certificates will be used in application properties.

keytool -keystore kafka.client.keystore.jks -alias localhost -validity 365 -genkey

keytool -keystore kafka.client.keystore.jks -alias localhost -certreq -file cert-file

openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days 365 -CAcreateserial -passin pass:<password>

keytool -keystore kafka.client.keystore.jks -alias CARoot -import -file ca-cert

keytool -keystore kafka.client.keystore.jks -alias localhost -import -file cert-signed
