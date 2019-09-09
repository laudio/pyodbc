#!/bin/bash

set -e

# Download semver
sudo curl https://raw.githubusercontent.com/fsaintjacques/semver-tool/2.1.0/src/semver -o /usr/local/bin/semver && sudo chmod +x /usr/local/bin/semver

last_tag=$(git tag --sort=-creatordate | head -n 1)
new_tag=$(semver bump patch "$last_tag")
new_version=$(if [ "$BRANCH" == "master" ]; then echo "${new_tag}"; else echo "${new_tag}-${BRANCH}"; fi)

echo "Last Version: ${last_tag}"
echo "New Version: ${new_version}"

git tag "${new_version}"

# Create image tag
image_tag="${IMAGE_NAME}:${new_version}"
docker tag "${IMAGE_NAME}" "${image_tag}"

echo "Tagged docker image $image_tag"

# If the branch is master, publish it.
if [ "$BRANCH" == "master" ]; then
  # Login to Docker
  echo "${DOCKER_REGISTRY_PASSWORD}" | docker login -u "${DOCKER_REGISTRY_USERNAME}" --password-stdin

  # Push the newly tagged image to registry and GitHub
  docker push "${image_tag}"
  docker push "${IMAGE_NAME}:latest"
  git push origin "${new_version}"

  echo "Published image $image_tag"
else
  echo "Publish skipped"
fi
