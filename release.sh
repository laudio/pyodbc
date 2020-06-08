#!/bin/bash

set -e


printfln() {
  printf "\n$1\n"
}

# TRAVIS_COMMIT_RANGE is usually invalid for force pushes - ignore such values
# This is just a safe guard against force push on the main branch(s).
if [ -n "$TRAVIS_COMMIT_RANGE" ]; then
  if ! git rev-list "$TRAVIS_COMMIT_RANGE" >/dev/null; then
    TRAVIS_COMMIT_RANGE=
  fi
fi

# Find all the commits for the current build
if [ -n "$TRAVIS_COMMIT_RANGE" ]; then
  COMMIT_RANGE="${TRAVIS_COMMIT_RANGE/.../..}"
fi

printfln "Commit range: $COMMIT_RANGE"

git log --oneline $COMMIT_RANGE

# Get the modified files if any
changed_files=$(git diff --name-only $TRAVIS_COMMIT_RANGE)
printfln "Changed file: $changed_files"

important_file_pattern=(Dockerfile requirements.txt)

# Loops for each file changes mentioned break if any found
for file in ${important_file_pattern[@]}; do
  changed_file=$(git diff --name-only $TRAVIS_COMMIT_RANGE | sort -u | grep -oP "$file" | cat)
  if [ -n "$changed_file" ]; then
    printfln "Changes detected in: $changed_file"
    changed=1
    break
  fi
done

if [ -z "$changed" ]; then
  echo "No changes detected, skipping release!"
  exit 0
fi

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
