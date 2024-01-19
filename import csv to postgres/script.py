import pandas as pd
import psycopg2
from io import StringIO

# PostgreSQL connection details
postgres_host = 'localhost'
postgres_port = '5432'
postgres_db = "mydb"
postgres_user = "postgres"
postgres_password = "postgres"

# Ask for the URL of the CSV file
google_sheets_url = input("Enter the URL of the CSV file: ")

# Ask for the table name
table_name = input("Enter the name of the table: ")

# Read the CSV file from the URL
df = pd.read_csv(google_sheets_url)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=postgres_host,
    port=postgres_port,
    database=postgres_db,
    user=postgres_user,
    password=postgres_password
    )

# Create a cursor object
cursor = conn.cursor()

# Map pandas data types to PostgreSQL data types
data_type_mapping = {
    "object": "text",
    "int64": "integer",
    "float64": "float",
    "bool": "boolean",
    "datetime64[ns]": "timestamp"
}

# Generate a string that defines the columns for the PostgreSQL table
columns = ", ".join([f'"{column_name}" {data_type_mapping[str(data_type)]}' for column_name, data_type in df.dtypes.items()])

# Get all column names
all_column_names = ', '.join([f'"{column_name}"' for column_name in df.columns])

# Drop the table if it exists
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# Create table if it doesn't exist
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {columns},
        CONSTRAINT unique_row UNIQUE({all_column_names})
    )
""")

# Get the current table structure
cursor.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
existing_columns = [row[0] for row in cursor.fetchall()]

# Get the columns from the CSV file
csv_columns = df.columns.tolist()

# Find the columns that are in the CSV file but not in the table
new_columns = set(csv_columns) - set(existing_columns)

# Add the new columns to the table
for column_name in new_columns:
    data_type = data_type_mapping[str(df[column_name].dtype)]
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS \"{column_name}\" {data_type}")

# Create a string buffer to hold CSV data
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False, header=False, sep="\t")
csv_buffer.seek(0)

# Create a temporary table
cursor.execute(f"""
    CREATE TEMP TABLE temp_table AS SELECT * FROM {table_name} LIMIT 0
""")

# Copy data from CSV buffer to temporary table
cursor.copy_expert(f"""
    COPY temp_table FROM STDIN WITH CSV DELIMITER '\t' NULL '' ESCAPE '\\' QUOTE '\"'
""", csv_buffer)

# Insert data from temporary table to main table, skipping duplicate rows
cursor.execute(f"""
    INSERT INTO {table_name}
    SELECT * FROM temp_table
    ON CONFLICT ON CONSTRAINT unique_row DO NOTHING
""")
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

# Print success message
print(f"Data imported successfully into {table_name}!")