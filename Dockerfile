FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
# Запуск від непривілейованого користувача; каталог для БД належить йому
RUN useradd --create-home --uid 10001 appuser && mkdir -p /data && chown appuser /data
USER appuser
ENV FLASK_APP=src/app.py DB_PATH=/data/demo.sqlite3
EXPOSE 5000
CMD ["/bin/sh", "-c", "python src/db.py && flask run --host=0.0.0.0 --port=5000"]
