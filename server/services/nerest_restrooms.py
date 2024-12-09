from pyspark.sql import SparkSession

# Initialize Spark Session (shared across API calls)
spark = (
    SparkSession.builder.appName("NearestPlacesFinder")
    .config("spark.driver.memory", "2g")
    .config("spark.executor.memory", "2g")
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop:9000")
    .config("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-client:3.3.1")
    .getOrCreate()
)


# Function to find nearest restrooms
def find_nearest_restrooms(x, y, n):
    hdfs_file_path = "hdfs://hadoop:9000/user/hdfs/uploads/all_restrooms.csv"
    restrooms_df = spark.read.csv(hdfs_file_path, header=True, inferSchema=True)
    restrooms_df.createOrReplaceTempView("restrooms")

    query = f"""
    SELECT name, latitude, longitude, address,
           (3958.8 * acos(
               cos(radians({x})) * cos(radians(latitude)) *
               cos(radians(longitude) - radians({y})) +
               sin(radians({x})) * sin(radians(latitude))
           )) AS distance
    FROM restrooms
    ORDER BY distance ASC
    LIMIT {n}
    """
    result_df = spark.sql(query)
    return result_df.collect()
