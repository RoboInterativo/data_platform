# Генерация ключа для сервера
openssl genrsa -out server-key.pem 2048

# Создание CSR (Certificate Signing Request)
openssl req -new -key server-key.pem -out server.csr \
-subj "/C=RU/ST=Moscow/L=Moscow/O=MyCompany/CN=kafka-server.mycompany.com"

# Добавление альтернативных имен (SANs)
echo subjectAltName = DNS:kafka-server.mycompany.com,DNS:kafka-server-1.mycompany.com,DNS:kafka-server-2.mycompany.com,DNS:kafka-server-3.mycompany.com > extfile.cnf

# Подписание CSR с использованием корневого сертификата
openssl x509 -req -in server.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -days 3650 -extfile extfile.cnf
