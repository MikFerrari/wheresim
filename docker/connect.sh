#!/bin/bash
CONTAINER_NAME="${1:-where2026}"

docker exec -it "$CONTAINER_NAME" /bin/bash