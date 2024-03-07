#!/bin/bash

docker build -f Dockerfile.freeze -t mplus-api-freezer .
docker run -it mplus-api-freezer > requirements-frozen.txt