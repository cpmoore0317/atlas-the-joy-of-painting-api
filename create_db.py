import pymysql

# Configuration for the MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
}

# Connect without specifying the database first
connection = pymysql.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password']
)

# Function to create the database
def create_database():
    create_db_script = "CREATE DATABASE IF NOT EXISTS joy_of_painting;"
    with connection.cursor() as cursor:
        cursor.execute(create_db_script)
        connection.commit()
    print('Database joy_of_painting created successfully.')

# Function to close the MySQL connection
def close_connection():
    connection.close()
    print('MySQL connection closed.')

# Initialize the database connection and execute the SQL script
try:
    create_database()
finally:
    close_connection()
