docker run \
  -e BOOTSTRAP_SERVERS='192.168.0.4:19092' \
  -e GROUP_ID=1 \
  -e CONFIG_STORAGE_TOPIC=my_connect_configs \
  -e OFFSET_STORAGE_TOPIC=my_connect_offsets \
  -e STATUS_STORAGE_TOPIC=my_connect_statuses  debezium/connect:1.2
