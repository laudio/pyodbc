TMP_PATH := .tmp
IMAGE_NAME := laudio/pyodbc

clean:
	@rm -rf $(TMP_PATH) __pycache__ .pytest_cache
	@find . -name '*.pyc' -delete

build:
	@docker buildx build --target=main -t $(IMAGE_NAME) .
	@docker buildx build --target=test -t $(IMAGE_NAME):test .

test:
	@docker run --env-file=./.env.test --network=host $(IMAGE_NAME):test

lint-examples:
	@docker build --target=lint-examples -t $(IMAGE_NAME):lint-examples .
	@docker run $(IMAGE_NAME):lint-examples

.PHONY: all test clean
