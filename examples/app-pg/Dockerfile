FROM laudio/pyodbc:latest

WORKDIR /app

# Copy code to container
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
