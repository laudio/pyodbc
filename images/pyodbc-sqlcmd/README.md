# pyodbc-sqlcmd

An alternative image which extends laudio/pyodbc and includes sqlcmd CLI.

https://hub.docker.com/r/laudio/pyodbc

## Usage

#### Pull the image

```bash
$ docker pull laudio/pyodbc:2.0.0-sqlcmd
```

#### Using as a base image

Usually this is expected to be used as a base image for your python app or scripts that requires pyodbc; in such such your `Dockerfile` might look something like this:

```Dockerfile
FROM laudio/pyodbc:2.0.0-sqlcmd

WORKDIR /source

# Add your source files.
COPY ["app", "./app"]
COPY ["setup.py", "./"]

RUN pip install .

CMD ["python", "app/main.py"]
```

## Development

```bash
# 1. Clone this repository.
$ git clone git@github.com:laudio/pyodbc.git

# 2. Go to the cloned path.
$ cd pyodbc/images/pyodbc-sqlcmd

# 3. Build a docker image.
$ make build

# 4. Run the container
$ docker run laudio/pyodbc-sqlcmd:<tag>
```

## Testing

You can build the test container image providing the flag `--target=test` and run it.

```bash
# Create .env.test file with your database connection creds
# using the the example file .env.example.
# You'll need to update .env.test with your values after this.
$ cp .env.example .env.test

# Build the test container image and run tests.
$ make clean build test
```

## License

Licensed under [MIT](LICENSE).
