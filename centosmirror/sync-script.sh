#!/bin/bash

# Репозитории для зеркалирования
BASE="https://mirror.yandex.ru/centos-stream"
REPO_BASEOS="$BASE/9-stream/BaseOS/x86_64/os/"
REPO_APPSTREAM="$BASE/9-stream/AppStream/x86_64/os/"

# Синхронизация BaseOS
rsync -avz --delete --exclude='repodata' -v \
  rsync://mirror.centos.org/centos/9-stream/BaseOS/x86_64/os/ \
  /mirror/baseos

# Синхронизация AppStream
rsync -avz --delete --exclude='repodata' -v \
  rsync://mirror.centos.org/centos/9-stream/AppStream/x86_64/os/ \
  /mirror/appstream

# Обновление метаданных
createrepo_c --update /mirror/baseos
createrepo_c --update /mirror/appstream
