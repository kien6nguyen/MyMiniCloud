FROM python:3.9-slim
RUN apt-get update && apt-get install -y libpq-dev gcc
WORKDIR /app
COPY . /app
RUN pip install flask psycopg2-binary
EXPOSE 5000
CMD ["python", "app.py"]
