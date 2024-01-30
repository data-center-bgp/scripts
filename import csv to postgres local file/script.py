import pandas as pd
import psycopg2
from io import StringIO

# PostgreSQL connection details
postgres_host = 'localhost'
postgres_port = '5432'
postgres_db = "mydb"
postgres_user = "postgres"
postgres_password = "postgres"

try:
    # Ask for the URL of the CSV file
    csv_file_name = input("Enter the name of CSV file: ")

    # Ask for the table name
    table_name = input("Enter the name of the table: ")

    # Ask for unique index column
    unique_index_column = input("Enter the name of the unique index column: ")

    # Ask for the CSV delimiter
    print("Select the delimiter of the CSV file:")
    print("1. Comma (,)")
    print("2. Semicolon (;)")
    print("3. Tab (\\t)")
    print("4. Pipe (|)")
    delimiter_option = input("Enter your choice: ")

    # Map the delimiter choice to the actual delimiter character
    delimiter_mapping = {
        "1": ",",
        "2": ";",
        "3": "\t",
        "4": "|"
    }
    delimiter = delimiter_mapping.get(delimiter_option)

    # Ask for the encoding of the CSV file
    print("Select the encoding of the CSV file:")
    print("1. UTF-8")
    print("2. latin-1")
    print("3. ascii")
    print("4. cp1252")
    encoding_option = input("Enter your choice: ")

    # Map the encoding choice to the actual encoding string
    encoding_mapping = {
        "1": "utf-8",
        "2": "latin-1",
        "3": "ascii",
        "4": "cp1252"
    }
    encoding = encoding_mapping.get(encoding_option)

    # Read the CSV file from the URL
    df = pd.read_csv(csv_file_name, low_memory=False, on_bad_lines='skip', sep=delimiter, encoding=encoding)

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

    unique_index_column = f'"{unique_index_column}"'

    # Generate a unique name for the constraint
    constraint_name = f"unique_row_{table_name}"

    # Drop the table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create table if it doesn't exist
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns},
            CONSTRAINT {constraint_name} UNIQUE({unique_index_column})
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
        ON CONFLICT ON CONSTRAINT {constraint_name} DO NOTHING
    """)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Print success message
    print(f"Data imported successfully into {table_name}!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    input("Press Enter to close...")