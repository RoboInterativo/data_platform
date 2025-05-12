FROM  moongeun/centos9:1.1


# Установка зависимостей
RUN dnf install -y \
    dnf-plugins-core \
    reposync \
    createrepo_c \
    nginx \
    cronie \
    rsync \
    && dnf clean all

# Настройка директорий
RUN mkdir -p /mirror/baseos /mirror/appstream
COPY nginx.conf /etc/nginx/nginx.conf
COPY sync-script.sh /sync-script.sh

# Разрешения и инициализация
RUN chmod +x /sync-script.sh
#    && createrepo_c /mirror/baseos \
#    && createrepo_c /mirror/appstream

# Запуск синхронизации при старте + веб-сервер
CMD /sync-script.sh && nginx -g "daemon off;"
