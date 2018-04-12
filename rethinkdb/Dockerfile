FROM alpine:latest

ARG BUILD_DATE
ARG VCS_REF
ARG RETHINKDB_VERSION=2.3.6

RUN apk --no-cache upgrade &&\
    apk --no-cache add \
    rethinkdb\
    su-exec &&\
    mkdir /data &&\
    chown daemon:daemon /data &&\
    apk --no-cache info -v | sed "s/-r\d*$//g"|sed 's/\(.*\)-/\1 /' > /etc/manifest.txt
  
VOLUME ["/data"]

WORKDIR /data

COPY ./entry.sh /usr/local/bin/entry.sh

ENTRYPOINT /usr/local/bin/entry.sh

#Ports:	process cluster webui
EXPOSE	28015 	29015 	8080