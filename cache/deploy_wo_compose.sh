#!/bin/bash

CONTAINER_NAME="AudioTagLoader"
IMAGE="redis:7-alpine"
HOST_PORT=6379
CONTAINER_PORT=6379
REDIS_PASSWORD="REDIS_PASSWORD"

HOST_DATA_DIR="/volume1/docker/Containers/AudioTagLoader/data"
HOST_CONF_FILE="/volume1/docker/Containers/AudioTagLoader/redis.conf"

docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  -p ${HOST_PORT}:6379 \
  -v "${HOST_DATA_DIR}:/data" \
  -v "${1}:/redis.conf:ro" \å
  "$IMAGE" \
  redis-server /redis.conf --requirepass "$REDIS_PASSWORD"