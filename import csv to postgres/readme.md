# CSV to PostgreSQL Importer

This script imports data from a CSV file into a PostgreSQL database.

## How it works

1. The script first asks for the URL of the CSV file and the name of the table where the data will be imported.
2. It reads the CSV file from the URL using pandas.
3. It connects to a PostgreSQL database using psycopg2.
4. It creates a mapping of pandas data types to PostgreSQL data types.
5. It generates a string that defines the columns for the PostgreSQL table based on the data types in the CSV file.
6. It drops the table if it already exists and creates a new one with the same name.
7. It gets the current table structure and the columns from the CSV file.
8. It finds the columns that are in the CSV file but not in the table and adds them to the table.
9. It creates a string buffer to hold the CSV data and copies it into a temporary table.
10. It inserts the data from the temporary table into the main table, skipping duplicate rows.
11. Finally, it closes the cursor and the connection and prints a success message.

## Requirements

- pandas
- psycopg2

## Usage

Run the script and enter the URL of the CSV file and the name of the table when prompted.

## Note

The script assumes that the PostgreSQL server is running on localhost and the port is 5432. The database name, username, and password are all "postgres". You may need to modify these values according to your setup.