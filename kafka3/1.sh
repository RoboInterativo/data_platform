#https://help.hcl-software.com/unica/Journey/en/12.1.0/Journey/AdminGuide/Configuration_of_kafka_on_SSL.html

  #  To deploy SSL, generate the key and the certificate for each machine in the cluster. Generate the key into a temporary keystore initially so that you can export and sign it later with CA.
    keytool -keystore kafka.server.keystore.jks -alias localhost -validity 365 -genkey
#  #      keystore: The keystore file that stores the certificate. The keystore file contains the private key of the certificate; therefore, it needs to be kept safely.
#        validity: The valid time of the certificate in days.
#    Create your own CA (certificate authority)

    openssl req -new -x509 -keyout ca-key -out ca-cert -days 365

#    The generated CA is simply a public-private key pair and certificate, and it is intended to sign other certificates.
#    Add the generated CA to the clients’ trust store so that the clients can trust this CA.
        keytool -keystore kafka.server.truststore.jks -alias CARoot -import -file ca-cert
        keytool -keystore kafka.client.truststore.jks -alias CARoot -import -file ca-cert
#    Sign all certificates in the keystore with the CA generated.
#        Export the certificate from the keystore:

        keytool -keystore kafka.server.keystore.jks -alias localhost -certreq -file cert-file
#    Sign it with CA.

    openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days 365 -CAcreateserial -passin pass:12345678
#    Import both the certificates of the CA and the signed certificate into the keystore.

    keytool -keystore kafka.server.keystore.jks -alias CARoot -import -file ca-cert

    keytool -keystore kafka.server.keystore.jks -alias localhost -import -file cert-signed
#    Create client keystore and import both certificates of the CA and signed certificates to client keystore. These client certificates will be used in application properties.

    keytool -keystore kafka.client.keystore.jks -alias localhost -validity 365 -genkey

    keytool -keystore kafka.client.keystore.jks -alias localhost -certreq -file cert-file

    openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days 365 -CAcreateserial -passin pass:12345678

    keytool -keystore kafka.client.keystore.jks -alias CARoot -import -file ca-cert

    keytool -keystore kafka.client.keystore.jks -alias localhost -import -file cert-signed
