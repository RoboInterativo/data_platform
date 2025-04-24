# Добавьте удаленный целевой бакет на server1

#mc mb server2/test
#mc version enable server2/test

mc alias set server1 http://195.140.146.176:9000 minio minio123
mc alias set server2 http://185.43.7.214:9000 minio minio


# Создание правила репликации
mc replicate add server2/test \
  --remote-bucket server1/test \
  --priority 1

mc replicate ls server2/test
mc replicate status server2/test
