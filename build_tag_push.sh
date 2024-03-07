#!/bin/bash
docker build . -t mplus-image
docker tag mplus-image us-central1-docker.pkg.dev/mplus-title-dashboard/mplus-docker-repo/mplus-api
docker push us-central1-docker.pkg.dev/mplus-title-dashboard/mplus-docker-repo/mplus-api