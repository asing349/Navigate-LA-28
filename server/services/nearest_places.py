from pyspark.sql import SparkSession

# Initialize Spark Session (shared across API calls)
spark = SparkSession.builder \
    .appName("NearestPlacesFinder") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop:9000") \
    .getOrCreate()

# Function to find nearest places
def find_nearest_places(x, y, n):
    hdfs_file_path = "hdfs://hadoop:9000/user/hdfs/uploads/all_places.csv"
    places_df = spark.read.csv(hdfs_file_path, header=True, inferSchema=True)
    places_df.createOrReplaceTempView("places")

    query = f"""
    SELECT name, latitude, longitude, address,
           (3958.8 * acos(
               cos(radians({x})) * cos(radians(latitude)) *
               cos(radians(longitude) - radians({y})) +
               sin(radians({x})) * sin(radians(latitude))
           )) AS distance
    FROM places
    ORDER BY distance ASC
    LIMIT {n}
    """
    result_df = spark.sql(query)
    return result_df.collect()
