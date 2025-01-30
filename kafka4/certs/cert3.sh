# Генерация ключа для клиента
cd /opt/certs
openssl genrsa -out client-key.pem 2048

# Создание CSR (Certificate Signing Request)
openssl req -new -key client-key.pem -out client.csr \
-subj "/C=RU/ST=Moscow/L=Moscow/O=MyCompany/CN=kafka-client.mycompany.com"

# Подписание CSR с использованием корневого сертификата
openssl x509 -req -in client.csr -CA ca-cert.pem -CAkey ca-key.pem \
-CAcreateserial -out client-cert.pem -days 3650
