#!/bin/bash
CONTAINER_NAME="${1:-where2026}"
IMAGE_NAME="${2:-mfocchi/trento_lab_framework:locosim}"

xhost +local:root

docker run --name "$CONTAINER_NAME" --gpus all \
  --workdir="/root" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --device=/dev/dri:/dev/dri \
  --network=host --hostname=docker -it \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --privileged --shm-size 2g \
  --volume "$HOME/projects/where_legged_robots_2026:/root" \
  "$IMAGE_NAME"