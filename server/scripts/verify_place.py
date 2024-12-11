# server/scripts/verify_places.py

import psycopg2  # For connecting to and interacting with the PostgreSQL database


def verify_data():
    """
    Verify and inspect data in the 'places' table of the database.

    Workflow:
        1. Establish a connection to the PostgreSQL database.
        2. Execute SQL queries to:
            - Count the total rows in the 'places' table.
            - Group rows by 'types' and count the occurrences.
            - Preview the first 10 rows of the 'places' table.
        3. Print the results of each query.
        4. Handle any exceptions that occur during database operations.
        5. Ensure the database connection is closed after execution.

    Raises:
        Exception: For any errors that occur during database interaction.
    """
    try:
        # Connect to the database
        connection = psycopg2.connect(
            dbname="navigate_la28_db",  # Name of the database
            user="la28_user",          # Database username
            password="bigdata_la28",   # Database password
            host="localhost",          # Host where the database is running
            port=5433                  # Port on which the database is listening
        )
        cursor = connection.cursor()  # Create a cursor for executing SQL queries

        # Query 1: Count total rows in the 'places' table
        cursor.execute("SELECT COUNT(*) FROM places;")  # Execute SQL query
        total_rows = cursor.fetchone()[0]  # Fetch the result
        # Print the total rows
        print(f"Total rows in 'places' table: {total_rows}")

        # Query 2: Group rows by 'types' and count the occurrences
        # Execute SQL query
        cursor.execute("SELECT types, COUNT(*) FROM places GROUP BY types;")
        types_data = cursor.fetchall()  # Fetch all rows from the result
        print("Rows grouped by 'types':")
        for row in types_data:  # Loop through each group and print
            print(row)

        # Query 3: Preview the first 10 rows in the 'places' table
        cursor.execute("SELECT * FROM places LIMIT 10;")  # Execute SQL query
        preview_data = cursor.fetchall()  # Fetch the first 10 rows
        print("Preview of 'places' table:")
        for row in preview_data:  # Loop through each row and print
            print(row)

    except Exception as e:
        # Handle any exceptions that occur during database operations
        print(f"Error: {e}")
    finally:
        # Ensure the database connection is closed after execution
        if connection:
            cursor.close()  # Close the cursor
            connection.close()  # Close the connection to the database


if __name__ == "__main__":
    """
    Entry point for the script.

    Calls the `verify_data` function to inspect the 'places' table in the database.
    """
    verify_data()  # Execute the function to verify the data

# Usage instructions:
# 1. Open a bash terminal inside the backend container:
#    docker exec -it navigate_la_backend bash
# 2. Run the script:
#    python verify_places.py
