xhost +local:root; \
docker rm -f where2026 >/dev/null 2>&1 || true; \
docker run --name where2026 --gpus all \
--workdir="/root" \
--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
--device=/dev/dri:/dev/dri \
--network=host --hostname=docker -it \
--env="DISPLAY=$DISPLAY" \
--env="QT_X11_NO_MITSHM=1" \
--privileged --shm-size 2g --rm \
--volume $HOME/projects/where_legged_robots_2026:/root \
mfocchi/trento_lab_framework:locosim