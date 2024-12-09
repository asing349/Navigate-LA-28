import psycopg2


def verify_data():
    try:
        # Connect to the database
        connection = psycopg2.connect(
            dbname="navigate_la28_db",
            user="la28_user",
            password="bigdata_la28",
            host="localhost",
            port=5433
        )
        cursor = connection.cursor()

        # Total rows
        cursor.execute("SELECT COUNT(*) FROM places;")
        total_rows = cursor.fetchone()[0]
        print(f"Total rows in 'places' table: {total_rows}")

        # Group by types
        cursor.execute("SELECT types, COUNT(*) FROM places GROUP BY types;")
        types_data = cursor.fetchall()
        print("Rows grouped by 'types':")
        for row in types_data:
            print(row)

        # Preview data
        cursor.execute("SELECT * FROM places LIMIT 10;")
        preview_data = cursor.fetchall()
        print("Preview of 'places' table:")
        for row in preview_data:
            print(row)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    verify_data()

# docker exec -it navigate_la_backend python verify_places.py
