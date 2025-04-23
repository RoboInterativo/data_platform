# Добавьте удаленный целевой бакет на server1
server2=185.43.7.214
server1=195.140.146.176
mc admin bucket remote add $server2/test \
  http://$server1:9000/test \
  --service "replication" \
  --region "us-east-1" \
  --access-key minio \
  --secret-key minio123

# Создайте правило репликации
mc replicate add $server2/test \
  --remote-bucket http://$server1:9000/test \
  --replicate "delete,delete-marker,existing-objects" \
  --priority 1
