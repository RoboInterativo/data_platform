# Добавьте удаленный целевой бакет на server1
mc alias set server1 http://195.140.146.176:9000 minio minio123
mc alias set server2 http://185.43.7.214:9000 minio minio


# Алиасы серверов (должны быть созданы через mc alias заранее!)
SERVER1_ALIAS="server1"
SERVER2_ALIAS="server2"

# Добавление удаленного бакета
mc admin bucket remote add $SERVER2_ALIAS/test \
  $SERVER1_ALIAS/test \
  --service-type "replication" \
  --region "us-east-1" \
  --access-key minio \
  --secret-key minio123

# Создание правила репликации
mc replicate add $SERVER2_ALIAS/test \
  --remote-bucket $SERVER1_ALIAS/test \
  --replicate "delete,delete-marker,existing-objects" \
  --priority 1
