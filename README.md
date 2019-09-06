# pyodbc

Docker Image with python 3.6, pyodbc and mssql tools.

https://hub.docker.com/r/laudio/pyodbc

## Usage

```bash
$ docker pull laudio/pyodbc
```

## Development

1. Clone this repository.

   ```bash
   $ git clone git@github.com:laudio/pyodbc.git
   ```

2. Go to the cloned path.

   ```bash
   $ cd pyodbc
   ```

3. Build a docker image.

   ```bash
   $ docker build -t laudio/pyodbc:<tag> .
   ```

4. Run docker container.

   ```bash
   $ docker run laudio/pyodbc:<tag>
   ```
