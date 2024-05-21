FROM apache/airflow:2.8.1
#ENV PIP_INDEX_URL https://hdp-nx3.dellin.ru/repository/pipy-public/simple/

USER root

#debian.sources mariadb.list mssql-release.list pgdg.list

# RUN rm  /etc/apt/sources.list.d/* -f
# RUN echo "Types: deb \n\
# URIs: http://nexus.bia-tech.ru/repository/debian-bookworm \n\
# Suites: bookworm bookworm-updates  \n\
# Components: main \n\
# Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg \n\
#  \n\
# Types: deb \n\
# URIs: http://nexus.bia-tech.ru/repository/debian-bookworm-security \n\
# Suites: bookworm-security \n\
# Components: main \n\
# Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg "  > /etc/apt/debian.sources


# RUN echo -e "deb http://nexus.bia-tech.ru/repository/debian-bookworm/ bookworm main \n\
# deb http://nexus.bia-tech.ru/repository/debian-bookworm/ bookworm-updates main \n\
# deb http://nexus.bia-tech.ru/repository/debian-bookworm-security/ bookworm-security main \n\
# deb [arch=amd64,armhf,arm64] https://nexus.bia-tech.ru/repository/apt-microsoft-bullseye/ bullseye main" > /etc/apt/sources.list

#RUN curl https://nexus.bia-tech.ru/repository/microsoft-keys/microsoft.asc | apt-key add -

#echo "deb [arch=amd64,arm64] https://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > \
#       /etc/apt/sources.list.d/pgdg.list
# RUN echo "deb http://nexus.bia-tech.ru/repository/debian-bookworm bullseye main \n\
#     debhttp://nexus.bia-tech.ru/repository/debian-bullseye-updates/ bullseye-security main \n\
#     deb http://nexus.bia-tech.ru/repository/debian-bullseye-updates/ bullseye-updates main \n\
#     deb [arch=amd64,armhf,arm64] https://nexus.bia-tech.ru/repository/apt-microsoft-bullseye/ bullseye main" > /etc/apt/sources.list

# Install dependencies
RUN apt-get update

RUN ACCEPT_EULA=Y apt-get upgrade -y
RUN apt-get -y install curl gnupg wget
# Install Kerberos
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install krb5-locales libkrb5-3 libapache2-mod-auth-gssapi


#COPY microsoft.asc /tmp/microsoft.asc
# Add bia-tech.ru repository
RUN cat /etc/apt/sources.list.d/debian.sources
RUN echo "deb [arch=amd64,armhf,arm64] https://packages.microsoft.com/ubuntu/22.04/mssql-server-2022 jammy main" >>/etc/apt/sources.list.d/debian.sources
RUN ls /etc/apt/sources.list.d
#RUN cat /tmp/microsoft.asc |  gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
COPY microsoft-prod.gpg /usr/share/keyrings/microsoft-prod.gpg


# Install config for Kerberos
RUN apt-get -y -qq install krb5-config krb5-user
RUN mkdir -p /var/run/httpd
#COPY ./kerberos_conf/krb5.conf /etc/krb5.conf
RUN chmod -R 777 /var/run/httpd

#RUN apt-get -y install libodbc1 odbcinst1debian2

#RUN ACCEPT_EULA=Y apt-get install -y unixodbc-dev
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN ACCEPT_EULA=Y apt-get install -y sqlcmd

# RUN apt-get install -y netcat
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Install MySQL ODBC 8.0 Unicode Driver
#RUN wget http://nexus.bia-tech.ru/repository/raw/mysql/mysql-connector-odbc-8.0.31-linux-glibc2.27-x86-64bit.tar.gz
#RUN tar -xvf mysql-connector-odbc-8.0.31-linux-glibc2.27-x86-64bit.tar.gz
#RUN cp -r mysql-connector-odbc-8.0.31-linux-glibc2.27-x86-64bit/bin/* /usr/local/bin/
#RUN cp -r mysql-connector-odbc-8.0.31-linux-glibc2.27-x86-64bit/lib/* /usr/local/lib/
#RUN chmod 777 /usr/local/lib/libmy*
# RUN apt-get -y install libodbc1 odbcinst1debian2
#RUN rm -rf mysql-connector-odbc-8.0.31-linux-glibc2.27-x86-64bit \
#    && rm -rf mysql-connector-odbc-8.0.31-linux-glibc2.27-x86-64bit.tar.gz
#RUN myodbc-installer -a -d -n "MySQL ODBC 8.0 Driver" -t "Driver=/usr/local/lib/libmyodbc8w.so"
#RUN myodbc-installer -a -d -n "MySQL ODBC 8.0" -t "Driver=/usr/local/lib/libmyodbc8a.so"
#RUN ldd /usr/local/lib/libmyodbc8w.so

RUN apt-get update
# Verify the installed driver:
# RUN myodbc-installer -d -l
# If everything is ok you will see output like:
# ODBC Driver 17 for SQL Server
# MySQL ODBC 8.0 Driver
# MySQL ODBC 8.0


# # User init
# RUN mkdir -p /usr/src/home
# RUN groupadd -g 1005 hive
# RUN useradd --uid 1005 --gid 1005 --shell /bin/sh --create-home --home-dir /usr/src/home/cdc_user hive
# USER hive
# WORKDIR /usr/src/home/cdc_user
#clean
RUN apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow
# Copy application and files
COPY ./requirements/common-data.txt ./requirements.txt
COPY ./test_connect.py ./

#ENV PATH=$PATH:/usr/src/home/cdc_user/.local/bin

RUN python3 -m pip install --root-user-action=ignore -r ./requirements.txt
