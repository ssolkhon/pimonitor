FROM python:3.9-slim

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "./main.py"]
