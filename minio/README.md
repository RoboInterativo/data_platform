Настроим взаимную репликацию между двумя MinIO-серверами (назовем их `server1` и `server2`). Предполагается, что:

- MinIO Client (`mc`) установлен и настроен.
- Адрес `server1`: `http://server1.example.com:9000`
- Адрес `server2`: `http://server2.example.com:9000`
- Бакеты для репликации: `bucket1` (на обоих серверах).

### 1. Настройка MinIO Client
Добавьте оба сервера в конфигурацию `mc`:
```bash
mc alias set server1 http://server1.example.com:9000 ACCESS_KEY_1 SECRET_KEY_1
mc alias set server2 http://server2.example.com:9000 ACCESS_KEY_2 SECRET_KEY_2
```

### 2. Создайте бакеты с включенной версионизацией
На обоих серверах:
```bash
# На server1
mc mb server1/bucket1
mc version enable server1/bucket1

# На server2
mc mb server2/bucket1
mc version enable server2/bucket1
```

### 3. Настройте взаимную репликацию

#### а) Настройте репликацию с server1 → server2
```bash
# Создайте правило репликации
mc replicate add server1/bucket1   --remote-bucket server2/bucket1   --priority 1
```

#### б) Настройте репликацию с server2 → server1
```bash
# Создайте правило репликации
mc replicate add server2/bucket1   --remote-bucket server1/bucket1   --priority 1
```

### 4. Проверьте настройки
```bash
# Проверьте правила на server1
mc replicate ls server1/bucket1

# Проверьте правила на server2
mc replicate ls server2/bucket1
```

### 5. Тестирование
Загрузите файл на `server1` и убедитесь, что он появился на `server2`:
```bash
echo "test" > test.txt
mc cp test.txt server1/bucket1
mc ls server2/bucket1
```

```bash
#server1
mc replicate status server1/bucket1
#server2
mc replicate status server2/bucket1
```
![рис1](https://github.com/RoboInterativo/data_platform/tree/main/minio/media/fig1.png)
Повторите тест в обратном направлении.

### Важные замечания:
1. **Версии MinIO**: Убедитесь, что используется MinIO версии не ниже `RELEASE.2020-12-03T05-49-24Z`.
2. **Сеть**: Серверы должны быть доступны друг другу через сеть (проверьте порты и фаерволы).
3. **Права доступа**: Учетные записи должны иметь права `s3:ReplicateObject`, `s3:GetReplicationConfiguration` и другие необходимые разрешения.
4. **Имена бакетов**: Если имена бакетов разные, укажите их в параметрах `--remote-bucket`.

Если возникнут ошибки, проверьте логи MinIO и убедитесь, что все шаги выполнены корректно.
