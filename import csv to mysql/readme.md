# CSV to MySQL Importer

This script imports data from a CSV file into a MySQL database.

## How it works

1. The script first asks for the name of the CSV file and the name of the table where the data will be imported.
2. It creates a connection to a MySQL database using SQLAlchemy.
3. It reads the CSV file using pandas.
4. It attempts to write the data to a table in the MySQL database. If the table already exists, it will be replaced.
5. If the data is imported successfully, it prints a success message. If an error occurs, it prints an error message.

## Requirements

- pandas
- SQLAlchemy
- mysql-connector-python

## Usage

Run the script and enter the name of the CSV file and the name of the table when prompted.

## Note

The script assumes that the MySQL server is running on localhost. The username is "root", the password is "mysql", and the database name is "mydb". You may need to modify these values according to your setup.