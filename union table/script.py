import psycopg2
import pandas as pd

connection = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="postgres",
    password="postgres"
)

cursor = connection.cursor();

num_tables = int(input("Enter the number of tables to join: "))

tables = []
for i in range(num_tables):
    table_name = input(f"Enter the name of table {i+1}: ")
    tables.append(table_name)

new_table_name = input("Enter the new table name: ")

union_query = f"CREATE TABLE {new_table_name} AS SELECT * FROM {tables[0]}"
for table in tables[1:]:
    union_query += f" UNION ALL SELECT * FROM {table}"

cursor.execute(union_query)

connection.commit()

cursor.close()
connection.close()