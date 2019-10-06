#!/bin/bash

set -e

last_tag=$(git tag --sort=-creatordate | head -n 1)
new_tag=$(semver bump patch "$last_tag")
timestamp=$(date -u +%Y%m%d%H%M%S)
ref=$(echo "$BRANCH" | sed -e "s/[^a-zA-Z0-9]//g")
new_version=$(if [ "$ref" = "master" ]; then echo "${new_tag}"; else echo "${new_tag}-${ref}.$timestamp"; fi)

echo "Bump version: ${last_tag} -> ${new_version}"
git tag "${new_version}"

# Create image tag
image_tag="${IMAGE_NAME}:${new_version}"
docker tag "${IMAGE_NAME}" "${image_tag}"

echo "Tagged docker image $image_tag"

# If the branch is master, publish it.
if [ "$ref" = "master" ]; then
  # Login to Docker
  echo "${DOCKER_REGISTRY_PASSWORD}" | docker login -u "${DOCKER_REGISTRY_USERNAME}" --password-stdin

  # Push the newly tagged image to registry and GitHub
  docker push "${image_tag}"
  docker push "${IMAGE_NAME}:latest"
  hub release create "${new_version}" -m "${new_version}" || true

  echo "Published $image_tag"
else
  echo "Publish skipped"
fi
