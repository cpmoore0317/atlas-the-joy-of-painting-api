import pymysql
import pandas as pd

# Configuration for the MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': '',
    'autocommit': True
}

# Function to execute the SQL script
def run_sql_script():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    script_file_path = './sql/database_init.sql'
    try:
        with open(script_file_path, 'r', encoding='utf8') as file:
            sql_script = file.read()
        cursor.execute(sql_script)
        print('SQL script executed successfully.')
    except Exception as e:
        print(f'Error executing SQL script: {e}')
    finally:
        cursor.close()
        connection.close()
        print('MySQL connection closed.')

# Initialize the database connection and execute the SQL script
if __name__ == "__main__":
    run_sql_script()
