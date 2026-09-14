#!/bin/bash
CONTAINER_NAME="${1:-where2026}"

docker stop "$CONTAINER_NAME"