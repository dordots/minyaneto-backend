FROM ubuntu:17.04
MAINTAINER Sergey Yavich

ENV TERM xterm-color
ENV DEBIAN_FRONTEND noninteractive

# ------------- Set locale UTF-8 -------------
RUN apt update && apt install -y --no-install-recommends locales apt-utils && locale-gen en_US.UTF-8                                      
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
# ------------- Install tools-----------------
RUN apt install -y --no-install-recommends vim curl wget zip unzip python libpython-dev python-pip uwsgi
ADD python27_plugin.so /usr/lib/uwsgi/plugins/python27_plugin.so
RUN chmod 644 /usr/lib/uwsgi/plugins/python27_plugin.so && pip install --upgrade pip && pip install setuptools wheel

# ------------- Create src and data folders --
RUN /bin/bash -c "mkdir -p /srv/{data,src} && chown www-data:www-data /srv/data"

WORKDIR /srv/src
ADD . ./minyaneto-backend

WORKDIR /srv/src/minyaneto-backend/scripts
RUN sh ./setup.linux.sh

# ------------- CLEAN IMAGE ------------------
RUN apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHONPATH=/srv/src/minyaneto-backend

EXPOSE 80 443

# Entry command
ENTRYPOINT uwsgi --ini /srv/src/minyaneto-backend/minyaneto.ini
