docker   run -p 8083:8083 \
  -e BOOTSTRAP_SERVERS='192.168.0.4:29092' \
  -e GROUP_ID=1 \
  -e CONFIG_STORAGE_TOPIC=my_connect_configs \
  -e OFFSET_STORAGE_TOPIC=my_connect_offsets \
  -e STATUS_STORAGE_TOPIC=my_connect_statuses  -itd debezium/connect:1.2
