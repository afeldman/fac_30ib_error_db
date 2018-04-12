FROM alpine:latest

ARG DB_HOST

# base
RUN apk add --no-cache --upgrade \
    py-pip \
    python \
    python-dev \
    py-setuptools \
    musl \
    build-base \
    linux-headers \
    bash \
    && rm -rf /var/cache/apk/* \
    && if [[ ! -e /usr/bin/python ]];        then ln -sf /usr/bin/python2.7 /usr/bin/python; fi \
    && if [[ ! -e /usr/bin/python-config ]]; then ln -sf /usr/bin/python2.7-config /usr/bin/python-config; fi \
    && if [[ ! -e /usr/bin/easy_install ]];  then ln -sf /usr/bin/easy_install-2.7 /usr/bin/easy_install; fi \ 
    && easy_install pip \
    && if [[ ! -e /usr/bin/pip ]]; then ln -sf /usr/bin/pip2.7 /usr/bin/pip; fi

RUN pip install --upgrade pip \
    && pip install flask \
       rethinkdb

RUN mkdir -p /fac_30ib/asset

WORKDIR /fac_30ib

ADD wait-for-it.sh /usr/local/bin/wait_for_it
ADD bootstrap.py /fac_30ib/bootstrap.py
ADD main.py /fac_30ib/fac_30ib.py
ADD asset/fanuc_error.json /fac_30ib/asset/fanuc_error.json

RUN chmod 777 /fac_30ib/bootstrap.py \
    && chmod 777 /fac_30ib/fac_30ib.py \
    && chmod 777 /usr/local/bin/wait_for_it

ENV PATH=${PATH}:/fac_30ib/
ENV FLASK_APP=fac_30ib.py

EXPOSE 5000

