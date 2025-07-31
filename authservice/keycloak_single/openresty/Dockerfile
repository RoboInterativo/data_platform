FROM openresty/openresty:alpine-fat
RUN mkdir /var/log/nginx
RUN apk add --no-cache openssl-dev
RUN apk add --no-cache git
RUN apk add --no-cache gcc
RUN luarocks install lua-resty-openidc &&\
    luarocks install lua-resty-jwt &&\
    luarocks install lua-resty-http
    
ENTRYPOINT ["/usr/local/openresty/nginx/sbin/nginx", "-g", "daemon off;"]
