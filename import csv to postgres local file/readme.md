# Local CSV File to PostgreSQL Importer

This script imports data from local CSV file in your computer into a PostgreSQL database.

## Features

- User-friendly: The script prompts the user to enter the necessary information, such as the name of the CSV file, name of the table, unique index column, delimiter, and encoding of the CSV file.
- Flexible: The script can handle CSV files with different delimiters and encodings.
- Robust: The script uses a temporary table to avoid inserting duplicate rows into the main table. If an error occurs, it prints an error message and does not crash.

## How it works

1. The script prompts user to enter necessary information.
2. It reads the CSV file using pandas, handling any bad lines by skipping them.
3. It connects to a PostgreSQL database using psycopg2 and creates a cursor object.
4. It maps pandas data types to PostgreSQL data types.
5. It generates a string that defines the columns for the PostgreSQL table.
6. It drops the table if it exists and creates a new one.
7. It gets the current table structure and columns from the CSV file.
8. It finds the columns that are in the CSV file but not in the table and adds them to the table.
9. It creates a string buffer to hold CSV and a temporary table.
10. It copies data from the CSV buffer to the temporary table.
11. It inserts data from the temporary table to the main table, skipping duplicate rows.
12. If the data is imported successfully, it prints a success message. If an error occurs, it prints error message.

## Requirements

- Python 3
- pandas
- psycopg2

## Installation

1. Install Python 3 if you haven't already.
2. Install the required Python packages with pip:

```
bash
pip install pandas psycopg2
```

## Usage

1. Run the script in the terminal:
```
python script.py
```
2. Follow the prompts to enter the necessary information.

## Note
The script assumes that the PostgreSQL server is running on the localhost. The username is "postgres", password is "postgres", and the database name is "mydb". You may need to modify these values according to your setup.