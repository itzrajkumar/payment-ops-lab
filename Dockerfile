from python:3.9-slim
workdir /app
copy app.py .
expose 8000
cmd ["python", "app.py"]