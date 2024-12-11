from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    avg,
    count,
    desc,
    dense_rank,
    col,
    round,
    year,
    current_date,
    when,
    sum,
    size,
    countDistinct,
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
    FloatType,
)
import pandas as pd
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from yarl import URL as MultiHostUrl
import os
from dotenv import load_dotenv
import logging

# Setup logging and environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConfig:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "la28_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "bigdata_la28")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "navigate_la28_db")

    @property
    def database_url(self) -> str:
        logger.info(
            f"Attempting to connect to: {self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
        )
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                user=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=int(self.POSTGRES_PORT),
                path=f"/{self.POSTGRES_DB}",
            )
        )


class AnalyticsService:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.engine = create_async_engine(
            self.db_config.database_url, echo=True, future=True, pool_pre_ping=True
        )
        self.AsyncSessionFactory = async_sessionmaker(
            self.engine,
            autoflush=False,
            expire_on_commit=False,
        )
        self.spark = None  # Initialize as None

    def _get_spark(self):
        """Get or create Spark session"""
        if self.spark is None or self.spark._jsc.sc().isStopped():  # Check if stopped
            self.spark = self._initialize_spark()
        return self.spark

    def _initialize_spark(self):
        """Initialize Spark session"""
        try:
            # Set Java home if not set
            if not os.getenv("JAVA_HOME"):
                os.environ["JAVA_HOME"] = (
                    "/usr/lib/jvm/java-11-openjdk-amd64"  # Adjust path as needed
                )

            return (
                SparkSession.builder.appName("NavigateLA-Analytics")
                .config("spark.driver.memory", "2g")
                .config("spark.executor.memory", "2g")
                .config("spark.driver.bindAddress", "0.0.0.0")
                .config("spark.driver.host", "localhost")
                .config("spark.sql.shuffle.partitions", "2")
                .config(
                    "spark.jars.packages", "org.postgresql:postgresql:42.2.18"
                )  # Add PostgreSQL JDBC driver
                .config(
                    "spark.driver.extraJavaOptions", "-Xss4M"
                )  # Increase stack size
                .config("spark.executor.extraJavaOptions", "-Xss4M")
                .config(
                    "spark.sql.execution.arrow.pyspark.enabled", "true"
                )  # Enable Arrow optimization
                .master("local[*]")
                .enableHiveSupport()  # Add Hive support
                .getOrCreate()
            )
        except Exception as e:
            logger.error(f"Failed to initialize Spark session: {str(e)}")
            logger.error("Java Home: " + os.getenv("JAVA_HOME", "Not Set"))
            raise

    async def _fetch_table_data(self, table_name: str) -> pd.DataFrame:
        """Fetch data from a table asynchronously"""
        async with self.AsyncSessionFactory() as session:
            try:
                query = text(f"SELECT * FROM {table_name}")
                result = await session.execute(query)
                return pd.DataFrame(result.fetchall(), columns=result.keys())
            except Exception as e:
                logger.error(f"Error fetching data from {table_name}: {str(e)}")
                raise

    async def _load_data(self):
        """Load data from database into Spark DataFrames"""
        # Initialize Spark session first
        self.spark = self._get_spark()

        # Define schemas
        user_schema = StructType(
            [
                StructField("id", IntegerType(), False),
                StructField("username", StringType(), False),
                StructField("password", StringType(), False),
                StructField("dob", TimestampType(), True),
                StructField("country", StringType(), True),
            ]
        )

        review_schema = StructType(
            [
                StructField("id", IntegerType(), False),
                StructField("user_id", IntegerType(), False),
                StructField("place_id", IntegerType(), False),
                StructField("rating", IntegerType(), False),
                StructField("comment", StringType(), True),
            ]
        )

        bus_route_usage_schema = StructType(
            [
                StructField("id", IntegerType(), False),
                StructField("user_id", IntegerType(), False),
                StructField("origin_stop_id", IntegerType(), False),
                StructField("destination_stop_id", IntegerType(), False),
            ]
        )

        bus_stop_schema = StructType(
            [
                StructField("id", IntegerType(), False),
                StructField("stop_number", IntegerType(), False),
                StructField("line", StringType(), False),
                StructField("direction", StringType(), False),
                StructField("stop_name", StringType(), False),
                StructField("latitude", FloatType(), False),
                StructField("longitude", FloatType(), False),
                StructField("geometry", StringType(), False),
            ]
        )

        place_schema = StructType(
            [
                StructField("id", IntegerType(), False),
                StructField("name", StringType(), False),
                StructField("category", StringType(), True),
                StructField("latitude", FloatType(), False),
                StructField("longitude", FloatType(), False),
                StructField("description", StringType(), True),
            ]
        )

        # Fetch all data concurrently
        tables = ["users", "reviews", "bus_route_usage", "bus_stops", "places"]
        data = await asyncio.gather(
            *[self._fetch_table_data(table) for table in tables]
        )

        # Create Spark DataFrames with explicit schemas
        self.users_df = self.spark.createDataFrame(data[0], schema=user_schema)
        self.reviews_df = self.spark.createDataFrame(data[1], schema=review_schema)
        self.bus_route_usage_df = self.spark.createDataFrame(
            data[2], schema=bus_route_usage_schema
        )
        self.bus_stops_df = self.spark.createDataFrame(data[3], schema=bus_stop_schema)
        self.places_df = self.spark.createDataFrame(data[4], schema=place_schema)

        # Cache DataFrames
        self.users_df.cache()
        self.reviews_df.cache()
        self.bus_route_usage_df.cache()
        self.bus_stops_df.cache()
        self.places_df.cache()

    def analyze_top_attractions(self):
        """Analyze most reviewed attractions"""
        return (
            self.reviews_df.join(
                self.places_df, self.reviews_df.place_id == self.places_df.id, "inner"
            )
            .groupBy("place_id", "name", "category", "latitude", "longitude")
            .agg(
                count("*").alias("review_count"),
                round(avg("rating"), 2).alias("avg_rating"),
                round(avg(when(col("rating") >= 4, 1).otherwise(0)), 2).alias(
                    "high_rating_ratio"
                ),
            )
            .orderBy(desc("review_count"))
            .withColumn("rank", dense_rank().over(Window.orderBy(desc("review_count"))))
        )

    def analyze_user_demographics(self):
        """Analyze user demographics and their platform usage"""
        users_with_age = self.users_df.withColumn(
            "age", year(current_date()) - year("dob")
        ).withColumn(
            "age_group",
            when(col("age") < 25, "18-24")
            .when(col("age").between(25, 34), "25-34")
            .when(col("age").between(35, 44), "35-44")
            .when(col("age").between(45, 54), "45-54")
            .otherwise("55+"),
        )

        # Age-based analysis
        age_reviews = (
            users_with_age.join(
                self.reviews_df, users_with_age.id == self.reviews_df.user_id, "left"
            )
            .groupBy("age_group")
            .agg(
                count("rating").alias("total_reviews"),
                round(avg("rating"), 2).alias("avg_rating"),
                countDistinct("user_id").alias("active_reviewers"),
            )
            .filter(col("total_reviews") > 0)
            .orderBy(desc("total_reviews"))
        )

        age_bus_usage = (
            users_with_age.join(
                self.bus_route_usage_df,
                users_with_age.id == self.bus_route_usage_df.user_id,
                "left",
            )
            .groupBy("age_group")
            .agg(
                count("*").alias("total_trips"),
                countDistinct("user_id").alias("active_riders"),
                round(count("*") / countDistinct("user_id"), 1).alias("trips_per_user"),
            )
            .filter(col("active_riders") > 0)
            .orderBy(desc("total_trips"))
        )

        # Country-based analysis
        country_reviews = (
            self.users_df.join(
                self.reviews_df, self.users_df.id == self.reviews_df.user_id, "left"
            )
            .groupBy("country")
            .agg(
                count("rating").alias("total_reviews"),
                round(avg("rating"), 2).alias("avg_rating"),
                countDistinct("user_id").alias("active_reviewers"),
            )
            .filter(col("total_reviews") > 0)
            .orderBy(desc("total_reviews"))
        )

        country_bus_usage = (
            self.users_df.join(
                self.bus_route_usage_df,
                self.users_df.id == self.bus_route_usage_df.user_id,
                "left",
            )
            .groupBy("country")
            .agg(
                count("*").alias("total_trips"),
                countDistinct("user_id").alias("active_riders"),
                round(count("*") / countDistinct("user_id"), 1).alias("trips_per_user"),
            )
            .filter(col("active_riders") > 0)
            .orderBy(desc("total_trips"))
        )

        return {
            "age": {"reviews": age_reviews, "bus_usage": age_bus_usage},
            "country": {"reviews": country_reviews, "bus_usage": country_bus_usage},
        }

    def analyze_bus_patterns(self):
        """Analyze bus usage patterns"""
        # Most frequent routes
        frequent_routes = (
            self.bus_route_usage_df.join(
                self.bus_stops_df.alias("origin"),
                self.bus_route_usage_df.origin_stop_id == col("origin.id"),
            )
            .join(
                self.bus_stops_df.alias("destination"),
                self.bus_route_usage_df.destination_stop_id == col("destination.id"),
            )
            .groupBy("origin.line", "origin.stop_name", "destination.stop_name")
            .agg(
                count("*").alias("trip_count"),
                countDistinct("user_id").alias("unique_users"),
            )
            .orderBy(desc("trip_count"))
        )

        # Line popularity
        line_popularity = (
            self.bus_route_usage_df.join(
                self.bus_stops_df,
                self.bus_route_usage_df.origin_stop_id == self.bus_stops_df.id,
            )
            .groupBy("line")
            .agg(
                count("*").alias("total_trips"),
                countDistinct("user_id").alias("unique_users"),
                countDistinct("origin_stop_id").alias("stops_used"),
            )
            .orderBy(desc("total_trips"))
        )

        return frequent_routes, line_popularity

    def analyze_geographic_distribution(self):
        """Analyze geographic distribution"""
        # User distribution by country with review counts
        user_distribution = (
            self.users_df.join(
                self.reviews_df.select(
                    col("id").alias("review_id"), col("user_id"), col("rating")
                ),
                self.users_df.id == col("user_id"),
                "left",
            )
            .groupBy("country")
            .agg(
                countDistinct(col("id")).alias("user_count"),  # Count distinct users
                countDistinct(col("review_id")).alias(
                    "active_users"
                ),  # Count distinct reviews
                round(avg(when(col("rating").isNotNull(), 1).otherwise(0)), 2).alias(
                    "avg_reviews_per_user"
                ),
            )
            .orderBy(desc("user_count"))
        )

        # Popular bus stops
        popular_stops = (
            self.bus_route_usage_df.join(
                self.bus_stops_df.select(
                    col("id").alias("stop_id"),
                    col("stop_name"),
                    col("line"),
                    col("latitude"),
                    col("longitude"),
                ),
                self.bus_route_usage_df.origin_stop_id == col("stop_id"),
            )
            .groupBy("stop_name", "line", "latitude", "longitude")
            .agg(
                count("*").alias("usage_count"),
                countDistinct("user_id").alias("unique_users"),
            )
            .orderBy(desc("usage_count"))
        )

        return user_distribution, popular_stops

    async def get_top_attractions(self, min_rating=None, category=None, limit=10):
        """Get top attractions with optional filters"""
        try:
            self.spark = self._get_spark()  # Get or create spark session
            await self._load_data()
            query = self.analyze_top_attractions()

            if min_rating:
                query = query.filter(col("avg_rating") >= min_rating)
            if category:
                query = query.filter(col("category") == category)

            result_df = query.limit(limit).toPandas()
            return self._convert_to_json_serializable(result_df)
        finally:
            if self.spark:
                self.spark.stop()
                self.spark = None

    async def get_user_demographics(self):
        """Get user demographics analysis"""
        try:
            self.spark = self._get_spark()
            await self._load_data()
            demographics = self.analyze_user_demographics()

            return {
                "age": {
                    "reviews": self._convert_to_json_serializable(
                        demographics["age"]["reviews"].toPandas()
                    ),
                    "bus_usage": self._convert_to_json_serializable(
                        demographics["age"]["bus_usage"].toPandas()
                    ),
                },
                "country": {
                    "reviews": self._convert_to_json_serializable(
                        demographics["country"]["reviews"].toPandas()
                    ),
                    "bus_usage": self._convert_to_json_serializable(
                        demographics["country"]["bus_usage"].toPandas()
                    ),
                },
            }
        finally:
            if self.spark:
                self.spark.stop()
                self.spark = None

    async def get_bus_routes_analysis(self, min_trips=None, limit=10):
        """Get bus routes analysis with optional filters"""
        try:
            self.spark = self._get_spark()
            await self._load_data()
            frequent_routes, line_popularity = self.analyze_bus_patterns()

            if min_trips:
                frequent_routes = frequent_routes.filter(col("trip_count") >= min_trips)
                line_popularity = line_popularity.filter(
                    col("total_trips") >= min_trips
                )

            return {
                "frequent_routes": self._convert_to_json_serializable(
                    frequent_routes.limit(limit).toPandas()
                ),
                "line_popularity": self._convert_to_json_serializable(
                    line_popularity.limit(limit).toPandas()
                ),
            }
        finally:
            if self.spark:
                self.spark.stop()
                self.spark = None

    async def get_popular_stops(self, min_usage=None, line=None, limit=10):
        """Get popular bus stops with optional filters"""
        try:
            self.spark = self._get_spark()
            await self._load_data()
            _, popular_stops = self.analyze_geographic_distribution()

            if min_usage:
                popular_stops = popular_stops.filter(col("usage_count") >= min_usage)
            if line:
                popular_stops = popular_stops.filter(col("line") == line)

            result_df = popular_stops.limit(limit).toPandas()
            return self._convert_to_json_serializable(result_df)
        finally:
            if self.spark:
                self.spark.stop()
                self.spark = None

    async def get_geographic_distribution(self):
        """Get geographic distribution of users"""
        try:
            self.spark = self._get_spark()
            await self._load_data()
            user_distribution, _ = self.analyze_geographic_distribution()
            return self._convert_to_json_serializable(user_distribution.toPandas())
        finally:
            if self.spark:
                self.spark.stop()
                self.spark = None

    def _convert_to_json_serializable(self, df):
        """Convert Pandas DataFrame to JSON serializable format"""
        if df is None:
            return None

        # Convert DataFrame to records and handle numpy types
        return df.astype(object).to_dict(orient="records")


analytics_service = AnalyticsService()
