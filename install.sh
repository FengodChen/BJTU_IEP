#! /bin/bash

# [Config]
export SERVER_NAME='fengodchen_apache_server'
export SERVER_VERSION='v1.0'
export SERVER_PORT=10

export SMR_PATH=$(pwd)

# [Shell]

# Install Server
docker build -t ${SERVER_NAME}:${SERVER_VERSION} App/Server/docker/ --rm \
    && docker run -it -p ${SERVER_PORT}:80 -v ${SMR_PATH}/Share:/Share ${SERVER_NAME}:${SERVER_VERSION}