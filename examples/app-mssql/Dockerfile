FROM laudio/pyodbc:1.0.8

WORKDIR /app

# Copy code to container
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
