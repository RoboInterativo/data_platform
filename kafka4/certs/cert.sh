# Создаем директорию для хранения ключей и сертификатов
#https://docs.cloudera.com/runtime/7.2.0/kafka-securing/topics/kafka-secure-sign-cert.html
# mkdir -p /etc/kafka/ssl && cd /etc/kafka/ssl
cd /opt/certs
# Генерация ключа для корневого CA
openssl genrsa -out ca-key.pem 2048

# Генерация корневого сертификата
openssl req -x509 -new -nodes -key ca-key.pem -sha256 -days 3650 \
-out ca-cert.pem \
-subj "/C=RU/ST=Moscow/L=Moscow/O=MyCompany/CN=Kafka Root CA"
