#! /bin/bash

# [Config]
source config

# [Shell]

# Install Server
docker build -t ${DOCKER_NAME}:${DOCKER_VERSION} App/Server/docker/ --rm \
    && docker run -itd -p ${DOCKER_PORT}:80 -v ${SMR_PATH}/Share:/Share -v ${SMR_PATH}/App/Server/html:/var/www/html --name ${SERVER_NAME} ${DOCKER_NAME}:${DOCKER_VERSION} \
    && docker start ${SERVER_NAME}