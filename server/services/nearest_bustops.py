from pyspark.sql import SparkSession
from shapely.geometry import LineString, Point
from shapely.ops import substring
import json

# Initialize Spark Session with HDFS configuration
spark = (
    SparkSession.builder.appName("DirectBusLinesFinder")
    .config("spark.driver.memory", "2g")
    .config("spark.executor.memory", "2g")
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop:9000")
    .config("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-client:3.3.1")
    .getOrCreate()
)


def trim_route_geometry(route_coords, origin_point, destination_point):
    """
    Extracts the portion of route geometry between origin and destination points.
    Returns only the route coordinates without including the origin and destination points.
    """
    # Create LineString from route coordinates
    route_line = LineString(route_coords)

    # Find the nearest points on the route to origin and destination
    origin_dist = route_line.project(Point(origin_point))
    dest_dist = route_line.project(Point(destination_point))

    # Ensure origin comes before destination
    start_dist = min(origin_dist, dest_dist)
    end_dist = max(origin_dist, dest_dist)

    # Extract the portion of the route between these points
    trimmed_line = substring(route_line, start_dist, end_dist)

    # Get the coordinates without adding origin and destination points
    return list(trimmed_line.coords)


async def find_direct_bus_lines(
    user_lat, user_lon, target_lat, target_lon, buffer_radius_miles
):
    """
    Finds the best direct bus route connecting user and target areas within a buffer radius.
    Returns the route with the shortest total distance to both stops.
    """
    try:
        # Read bus stops data
        hdfs_file_path = "hdfs://hadoop:9000/user/hdfs/uploads/bus_stops.csv"
        bus_stops_df = spark.read.csv(hdfs_file_path, header=True, inferSchema=True)
        bus_stops_df.createOrReplaceTempView("bus_stops")

        # Query to find stops near user location
        user_query = f"""
        SELECT STOPNUM, LINE, DIR, STOPNAME, LAT, LONG,
               (3958.8 * acos(
                   cos(radians({user_lat})) * cos(radians(LAT)) *
                   cos(radians(LONG) - radians({user_lon})) +
                   sin(radians({user_lat})) * sin(radians(LAT))
               )) AS distance
        FROM bus_stops
        WHERE (3958.8 * acos(
                   cos(radians({user_lat})) * cos(radians(LAT)) *
                   cos(radians(LONG) - radians({user_lon})) +
                   sin(radians({user_lat})) * sin(radians(LAT))
               )) <= {buffer_radius_miles}
        """

        # Query to find stops near target location
        target_query = f"""
        SELECT STOPNUM, LINE, DIR, STOPNAME, LAT, LONG,
               (3958.8 * acos(
                   cos(radians({target_lat})) * cos(radians(LAT)) *
                   cos(radians(LONG) - radians({target_lon})) +
                   sin(radians({target_lat})) * sin(radians(LAT))
               )) AS distance
        FROM bus_stops
        WHERE (3958.8 * acos(
                   cos(radians({target_lat})) * cos(radians(LAT)) *
                   cos(radians(LONG) - radians({target_lon})) +
                   sin(radians({target_lat})) * sin(radians(LAT))
               )) <= {buffer_radius_miles}
        """

        # Execute queries
        user_stops = spark.sql(user_query).collect()
        target_stops = spark.sql(target_query).collect()

        # Read bus route geometries from HDFS using Spark's JSON reader
        geojson_path = "hdfs://hadoop:9000/user/hdfs/uploads/bus_lines.geojson"
        route_df = spark.read.option("multiline", "true").json(geojson_path)

        try:
            # Convert DataFrame to list of rows and extract features
            features = route_df.select("features").first()[0]

            # Create route geometry lookup with additional metadata
            route_lookup = {}
            for feature in features:
                route_num = str(feature.properties.RouteNumber)
                route_info = {
                    "geometry": feature.geometry.coordinates,
                    "name": feature.properties.RouteName,
                    "type": feature.properties.MetroBusType,
                    "category": feature.properties.MetroCategory,
                }

                # Store multiple variations of the same route number
                if route_num not in route_lookup:
                    route_lookup[route_num] = []
                route_lookup[route_num].append(route_info)

            # Find the best route by comparing total distances
            best_route = None
            min_total_distance = float("inf")
            best_stops = None

            for user_stop in user_stops:
                for target_stop in target_stops:
                    if user_stop.LINE == target_stop.LINE:
                        total_distance = user_stop.distance + target_stop.distance
                        route_variations = route_lookup.get(str(user_stop.LINE), [])

                        for route_info in route_variations:
                            # Create points for origin and destination
                            origin_point = Point(
                                float(user_stop.LONG), float(user_stop.LAT)
                            )
                            dest_point = Point(
                                float(target_stop.LONG), float(target_stop.LAT)
                            )
                            route_line = LineString(route_info["geometry"])

                            # Calculate distances from stops to route
                            origin_dist_to_route = origin_point.distance(route_line)
                            dest_dist_to_route = dest_point.distance(route_line)

                            # Add route proximity to total distance calculation
                            adjusted_total_distance = (
                                total_distance
                                + origin_dist_to_route
                                + dest_dist_to_route
                            )

                            if adjusted_total_distance < min_total_distance:
                                min_total_distance = adjusted_total_distance
                                best_route = {
                                    "route_number": user_stop.LINE,
                                    "route_name": route_info["name"],
                                    "route_type": route_info["type"],
                                    "category": route_info["category"],
                                    "geometry": trim_route_geometry(
                                        route_info["geometry"],
                                        [float(user_stop.LONG), float(user_stop.LAT)],
                                        [
                                            float(target_stop.LONG),
                                            float(target_stop.LAT),
                                        ],
                                    ),
                                    "origin": {
                                        "stop_number": user_stop.STOPNUM,
                                        "name": user_stop.STOPNAME,
                                        "distance": float(user_stop.distance),
                                        "coordinates": [
                                            float(user_stop.LONG),
                                            float(user_stop.LAT),
                                        ],
                                    },
                                    "destination": {
                                        "stop_number": target_stop.STOPNUM,
                                        "name": target_stop.STOPNAME,
                                        "distance": float(target_stop.distance),
                                        "coordinates": [
                                            float(target_stop.LONG),
                                            float(target_stop.LAT),
                                        ],
                                    },
                                }

        except Exception as e:
            print(f"Error processing route data: {str(e)}")
            print(f"Route DataFrame schema: {route_df.printSchema()}")
            print(f"Route DataFrame schema: {route_df.printSchema()}")
            raise

        if best_route is None:
            return {
                "status": "error",
                "data": {"message": "No direct bus routes found"},
            }

        # Restructure the response format
        return {
            "status": "success",
            "data": {
                "route_number": str(best_route["route_number"]),
                "route_name": best_route["route_name"],
                "route_type": best_route["route_type"],
                "category": best_route["category"],
                "geometry": best_route["geometry"],
                "origin": {
                    "stop_number": str(best_route["origin"]["stop_number"]),
                    "name": best_route["origin"]["name"],
                    "distance": round(best_route["origin"]["distance"], 2),
                    "coordinates": best_route["origin"]["coordinates"],
                },
                "destination": {
                    "stop_number": str(best_route["destination"]["stop_number"]),
                    "name": best_route["destination"]["name"],
                    "distance": round(best_route["destination"]["distance"], 2),
                    "coordinates": best_route["destination"]["coordinates"],
                },
            },
        }

    except Exception as e:
        print(f"Error finding direct bus lines: {str(e)}")
        return {
            "status": "error",
            "data": {"message": f"Error finding direct bus lines: {str(e)}"},
        }
