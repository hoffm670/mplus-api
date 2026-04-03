#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
git pull

docker build -f Dockerfile.pi . -t mplus-api

# Stop/remove any containers currently bound to port 8080
PORT_CONTAINERS=$(docker ps --filter "publish=8080" --format "{{.ID}}")
if [ -n "${PORT_CONTAINERS}" ]; then
  docker stop ${PORT_CONTAINERS}
  docker rm ${PORT_CONTAINERS}
fi

# Also stop/remove prior mplus-api by name if it exists
docker stop mplus-api 2>/dev/null || true
docker rm mplus-api 2>/dev/null || true

docker run -d --name mplus-api -p 8080:8080 mplus-api