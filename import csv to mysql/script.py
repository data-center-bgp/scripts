import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

host = 'localhost'
user = 'root'
password = 'mysql'
database = 'mydb'

# Ask the user for the CSV file name and the table name
csv_file_name = input("Please enter the CSV file name: ")
table_name = input("Please enter the table name: ")

# Create a connection to the database
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

# Read the CSV file
df = pd.read_csv(csv_file_name, delimiter=';', low_memory=False)

try:
    # Write the data to a table in the MySQL database
    df.to_sql(table_name, engine, if_exists='replace')
    print("Data imported successfully!")
except Exception as e:
    print(f"Failed to import data: {e}")