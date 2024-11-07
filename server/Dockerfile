FROM python:3.11.5
WORKDIR /app
COPY . .
RUN pip install boto3 fastapi fiona geopandas hdfs pandas pyarrow pyspark python-dotenv shapely uvicorn watchdog
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]