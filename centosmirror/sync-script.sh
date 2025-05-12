#!/bin/bash

# Репозитории для зеркалирования
REPO_BASEOS="https://mirror.stream.centos.org/9-stream/BaseOS/x86_64/os/"
REPO_APPSTREAM="https://mirror.stream.centos.org/9-stream/AppStream/x86_64/os/"

# Синхронизация BaseOS
rsync -avz --delete --exclude='repodata' \
  rsync://mirror.centos.org/centos/9-stream/BaseOS/x86_64/os/ \
  /mirror/baseos

# Синхронизация AppStream
rsync -avz --delete --exclude='repodata' \
  rsync://mirror.centos.org/centos/9-stream/AppStream/x86_64/os/ \
  /mirror/appstream

# Обновление метаданных
createrepo_c --update /mirror/baseos
createrepo_c --update /mirror/appstream
