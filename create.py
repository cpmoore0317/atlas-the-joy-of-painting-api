import pymysql
import os

# Configuration for the MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'joy_of_painting'
}

# Connect without specifying the database first
connection = pymysql.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    database=db_config['database']
)

# Function to create tables
def create_tables():
    script_file_path = './sql/database_init.sql'
    if os.path.exists(script_file_path):
        with open(script_file_path, 'r') as file:
            sql_script = file.read()
            statements = sql_script.split(';')
            with connection.cursor() as cursor:
                for statement in statements:
                    if statement.strip():
                        cursor.execute(statement)
                connection.commit()
                print('Tables created successfully.')

# Function to close the MySQL connection
def close_connection():
    connection.close()
    print('MySQL connection closed.')

# Initialize the database connection and execute the SQL script
try:
    create_tables()
finally:
    close_connection()
