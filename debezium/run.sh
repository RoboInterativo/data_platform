docker   run -p 8083:8083 \
  -e BOOTSTRAP_SERVERS='172.17.0.1:29092' \
  -e GROUP_ID=1 \
  -e CONFIG_STORAGE_TOPIC=my_connect_configs \
  -e OFFSET_STORAGE_TOPIC=my_connect_offsets \
  -e STATUS_STORAGE_TOPIC=my_connect_statuses  -itd debezium/connect:1.9
#  --add-host t-gp-cdc-db-1.dellin.local:10.214.66.156 \
  # -e KAFKA_OPTS="-Djava.security.auth.login.config=path/to/jaas.conf" \

#SASL_PLAINTEXT
#  -e CONNECT_SASL_JAAS_CONFIG='org.apache.kafka.common.security.plain.PlainLoginModule required username=\"admin\" password=\"admin-secret\";' \
#-e CONNECT_SECURITY_PROTOCOL=SASL_PLAINTEXT \
