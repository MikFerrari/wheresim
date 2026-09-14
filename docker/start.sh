#!/bin/bash
CONTAINER_NAME="${1:-where2026}"

docker start "$CONTAINER_NAME"
