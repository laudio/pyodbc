TMP_PATH := .tmp
IMAGE_NAME := laudio/pyodbc

clean:
	@rm -rf $(TMP_PATH) __pycache__ .pytest_cache
	@find . -name '*.pyc' -delete

build:
	@docker build --target=base -t $(IMAGE_NAME) .
	@docker build --target=test -t $(IMAGE_NAME):test .

test:
	@docker run --env-file=./.env.test --network=host $(IMAGE_NAME):test

lint-examples:
	@docker build --target=lint-examples -t $(IMAGE_NAME):lint-examples .
	@docker run $(IMAGE_NAME):lint-examples

check: 
	@pyright

.PHONY: all test clean
