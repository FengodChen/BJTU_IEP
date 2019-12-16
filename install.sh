#! /bin/bash

# [Config]
export SERVER_NAME='fengodchen_main'
export DOCKER_NAME='fengodchen_apache_server'
export DOCKER_VERSION='v1.0'
export DOCKER_PORT=10

export SMR_PATH=$(pwd)

# [Shell]

# Install Server
docker build -t ${DOCKER_NAME}:${DOCKER_VERSION} App/Server/docker/ --rm \
    && docker run -itd -p ${DOCKER_PORT}:80 -v ${SMR_PATH}/Share:/Share --name ${SERVER_NAME} ${DOCKER_NAME}:${DOCKER_VERSION} \
    && docker start ${SERVER_NAME}