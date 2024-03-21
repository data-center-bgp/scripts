import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection details
postgres_host = 'localhost'
postgres_port = '5432'
postgres_db = "mydb"
postgres_user = "postgres"
postgres_password = "postgres"

# List of Google Sheets CSV URLs
google_sheets_urls = [
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vS1pJFTY0-VBXC2IZLWbkM9aY4Mil_5t2rMVeQZFazJ7O8hqo7HlIiMRdOX8TAXueEPXp-dyRUSDsTq/pub?gid=1601108921&single=true&output=csv',
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8BWoTeRaIl8_VNrln_9rqiV28Gui-mnLzZJVwDRRIskTkQgJx7uqIZF_7ia8rH3DX1rnXoJbkYPTY/pub?gid=1601108921&single=true&output=csv',
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vR1R51rBeERAgxdLfkwdPf1t2cVtWETJuHaSzVIWW8iEIBwrwbVwM34lDQXscKz7_vOqknev_UZZ5Y7/pub?gid=1601108921&single=true&output=csv',
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vQoEgHKOXMkc-Kgl4dbCa9h_EGNmRBtFhj7SrDAoSqLvvuJYKBa5rBX-jmjY-Df8FHzsLi9GpnQVVIB/pub?gid=1601108921&single=true&output=csv'
]

# CSV delimiter and encoding
delimiter = ','
encoding = 'utf-8'

# Create a database connection
engine = create_engine(f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}')

# Loop over each URL in the list
for i, google_sheets_url in enumerate(google_sheets_urls, start=1):
    # Generate the table name based on the index of the URL
    table_name = f"table{i}"

    # Read the CSV file from the URL
    df = pd.read_csv(google_sheets_url, delimiter=delimiter, encoding=encoding)

    # Write the data to the database
    df.to_sql(table_name, engine, if_exists='replace')

    # Print a success message
    print(f"Data from {google_sheets_url} has been loaded into {table_name}.")