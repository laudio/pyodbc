#!/bin/bash

set -e

# Download semver
sudo curl https://raw.githubusercontent.com/fsaintjacques/semver-tool/2.1.0/src/semver -o /usr/local/bin/semver && sudo chmod +x /usr/local/bin/semver && semver --version

last_version=$(git tag --sort=-creatordate | head -n 1)
new_version=$(semver bump patch "$last_version")

git tag "$new_version"
# git push origin "$new_version"

# Login to Docker
echo ${DOCKER_REGISTRY_PASSWORD} | docker login -u $DOCKER_REGISTRY_USERNAME --password-stdin

# Publish to registry
image_tag="${IMAGE_NAME}:${new_version}"
docker tag "$IMAGE_NAME" "$image_tag"
# docker push "$image_tag"
# docker push "${IMAGE_NAME}:latest"
