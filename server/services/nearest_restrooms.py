# server/services/nearest_restrooms.py

# Import SparkSession for managing Spark DataFrames
from pyspark.sql import SparkSession

# Initialize Spark Session (shared across API calls)
spark = (
    # Name the Spark application
    SparkSession.builder.appName("NearestPlacesFinder")
    # Set memory allocation for the Spark driver
    .config("spark.driver.memory", "2g")
    # Set memory allocation for the Spark executor
    .config("spark.executor.memory", "2g")
    # Use HDFS as the default file system
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop:9000")
    # Configure HDFS implementation
    .config("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem")
    # Configure local file system implementation
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    # Include Hadoop client package
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-client:3.3.1")
    .getOrCreate()  # Create or retrieve the SparkSession
)

# Function to find nearest restrooms


def find_nearest_restrooms(x, y, n):
    """
    Find the nearest restrooms to a given location using the Haversine formula.

    Args:
        x (float): Latitude of the given location.
        y (float): Longitude of the given location.
        n (int): Number of nearest restrooms to return.

    Returns:
        list: A list of rows representing the nearest restrooms, including their names,
              coordinates, addresses, and distances.

    Steps:
        1. Load the dataset of restrooms from HDFS.
        2. Register the dataset as a temporary SQL table.
        3. Use SQL to calculate the distances to all restrooms using the Haversine formula.
        4. Sort the results by distance in ascending order and limit the results to the top `n` restrooms.
        5. Return the results as a list of rows.
    """
    # Path to the CSV file containing restroom data on HDFS
    hdfs_file_path = "hdfs://hadoop:9000/user/hdfs/uploads/all_restrooms.csv"

    # Read the CSV file into a Spark DataFrame
    restrooms_df = spark.read.csv(
        hdfs_file_path, header=True, inferSchema=True)

    # Register the DataFrame as a temporary SQL table
    restrooms_df.createOrReplaceTempView("restrooms")

    # SQL query to calculate distances and find the nearest restrooms
    query = f"""
    SELECT name, latitude, longitude, address,
           (3958.8 * acos(
               cos(radians({x})) * cos(radians(latitude)) *
               cos(radians(longitude) - radians({y})) +
               sin(radians({x})) * sin(radians(latitude))
           )) AS distance  -- Calculate distance using the Haversine formula
    FROM restrooms
    ORDER BY distance ASC  -- Sort results by distance (ascending)
    LIMIT {n}  -- Limit results to the top `n` restrooms
    """

    # Execute the query and collect the results
    result_df = spark.sql(query)
    return result_df.collect()  # Return the results as a list of rows
