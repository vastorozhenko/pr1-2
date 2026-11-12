
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
ENV FLASK_APP=src/app.py
ENV SECRET_KEY=dev-docker-secret
EXPOSE 5000
CMD ["python", "src/db.py"] && ["flask", "run", "--host=0.0.0.0", "--port=5000"]
