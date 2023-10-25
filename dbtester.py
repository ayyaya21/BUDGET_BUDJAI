import mysql.connector

# Replace these with your database connection details
db_config = {
    'user': 'root',
    'password': '6939',
    'host': 'localhost',
    'database': 'db',
}

# Connect to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

# Get the list of tables in the database
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# Iterate through the tables and retrieve their data
for table in tables:
    table_name = table['Tables_in_db']  # Replace 'db' with your actual database name

    # Select all rows from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    table_data = cursor.fetchall()

    print(f"Table: {table_name}")
    for row in table_data:
        print(row)

# Close the database connection
conn.close()