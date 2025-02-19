#!/bin/bash

image=("jg_webtext")
container=("jg")

echo "Processing container: ${container}..."

echo "Killing and removing old container..."
docker kill ${container}
docker rm ${container}
docker rmi ${image}

echo "Building new image..."
docker build -t ${image} .

docker run -d --name ${container} --volume ./outputs:/jg_webtext/outputs ${image}
