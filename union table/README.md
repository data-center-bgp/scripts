# PostgreSQL Table Union Script

This Python script allows you to create a new PostgreSQL table by performing a `UNION ALL` operation on a number of existing tables. The tables should have identical structure (i.e, the same columns with compatible data types). This is particularly useful when you have data spread across multiple tables for different periods or categories but with the same structure, and you want to combine them into a single table for easier analysis and operations.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed Python 3. If not, you can download it from [here](https://www.python.org/downloads/).
* You have installed the psycopg2 and pandas Python libraries. If not, you can install them using pip:

```bash
pip install psycopg2-binary pandas
```
* You have a PostgreSQL server running and accessible. If not, you can download and install it from [here](https://www.postgresql.org/download/)

## Using PostgreSQL Table Union Script

To use the script, follow these steps:

1. Update the connection parameters in the script to match your PostgreSQL server details:

```
connection = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="postgres",
    password="postgres"
)
```

2. Run the script:

```
python script.py
```

3. When prompted, enter the number of tables you want to join.
4. Enter the name of each table when prompted.
5. Enter the name of the new table that will be created.

The script will create a new table in your PostgreSQL database that contains all rows from the specified tables. If there are duplicate rows across tables, they will all be included in the new table.

## Contributing to PostgreSQL Table Union Script

To contribute to the script, follow these steps:

1. For this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`.
4. Push to the original branch: `git push origin <project_name>/<location>`.
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).