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

# Ask for the CSV delimiter
print("Select the CSV delimiter:")
print("1. Comma (,)")
print("2. Semicolon (;)")
print("3. Tab (\\t)")
print("4. Pipe (|)")
delimiter_option = input("Enter your choice: ")

# Map the delimiter option to the actual delimiter
delimiter_mapping = {
    "1": ",",
    "2": ";",
    "3": "\t",
    "4": "|"
}
delimiter = delimiter_mapping.get(delimiter_option)

# Ask for the CSV encoding
print("Select the CSV encoding:")
print("1. UTF-8")
print("2. latin-1")
print("3. ascii")
print("4. cp1252")
encoding_option = input("Enter your choice: ")

# Map the encoding option to the actual encoding
encoding_mapping = {
    "1": "utf-8",
    "2": "latin-1",
    "3": "ascii",
    "4": "cp1252"
}
encoding = encoding_mapping.get(encoding_option)

# Read the CSV file from the URL
df = pd.read_csv(google_sheets_url, low_memory=False, sep=delimiter, encoding=encoding)

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

# Drop the table if it exists
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# Create table
cursor.execute(f"""
    CREATE TABLE {table_name} (
        {columns}
    )
""")

# Create a string buffer to hold CSV data
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False, header=False, sep="\t")
csv_buffer.seek(0)

# Copy data from CSV buffer to table
cursor.copy_expert(f"""
    COPY {table_name} FROM STDIN WITH CSV DELIMITER '\t' NULL '' ESCAPE '\\' QUOTE '\"'
""", csv_buffer)

conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

# Print success message
print(f"Data imported successfully into {table_name}!")

# Pause the script
input("Press any key to exit...")