# Добавьте удаленный целевой бакет на server1

#mc mb server1/test
#mc version enable server1/test

mc alias set server1 http://195.140.146.176:9000 minio minio123
mc alias set server2 http://185.43.7.214:9000 minio minio


# Создание правила репликации
mc replicate add server1/test \
  --remote-bucket server2/test \
  --priority 1
  
mc replicate ls server2/test
mc replicate status server1/test
