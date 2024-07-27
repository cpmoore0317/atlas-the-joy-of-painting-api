import pymysql
import pandas as pd
import os

# Configuration for the MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'joy_of_painting'
}

# File paths
colors_used = './data/The Joy Of Painting - Colors Used'
episode_dates = './data/The Joy Of Painting - Subject Matter'

# Create a MySQL connection
try:
    connection = pymysql.connect(**db_config)
except pymysql.MySQLError as e:
    print(f"Error connecting to MySQL: {e}")
    raise

def read_csv_file(file_path, columns):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(f"Columns in {file_path}: {df.columns.tolist()}")  # Print columns for debugging
        if all(col in df.columns for col in columns):
            return df[columns].values.tolist()
        else:
            raise ValueError(f"None of the columns {columns} are in the DataFrame")
    else:
        raise FileNotFoundError(f"File {file_path} does not exist")

def colors_used_for_episodes():
    columns = ['painting_title', 'season', 'episode', 'img_src', 'youtube_src']
    return read_csv_file(colors_used, columns)

def dates_for_episodes():
    columns = ['EPISODE']  # Update to actual column name in the CSV file
    data = read_csv_file(episode_dates, columns)
    # Convert to list of strings if necessary
    return [str(episode[0]) for episode in data]

def merge_data(data1, data2):
    # Use None as a placeholder for missing air_date
    return [row1 + [None] for row1, row2 in zip(data1, data2)]

try:
    colors_data = colors_used_for_episodes()
    dates_data = dates_for_episodes()
    merged_data = merge_data(colors_data, dates_data)
    print(merged_data[:3])  # Print first few rows for debugging
    
    # Alter the table to allow NULL values for air_date
    alter_table_sql = "ALTER TABLE episodes MODIFY air_date DATE NULL"
    with connection.cursor() as cursor:
        cursor.execute(alter_table_sql)
        connection.commit()

    # Insert data into the database
    sql = """
    INSERT INTO episodes (title, season_number, episode_number, painting_img_src, painting_yt_src, air_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        for row in merged_data:
            cursor.execute(sql, tuple(row))
        connection.commit()
        print('Data inserted successfully into episodes table.')

except Exception as e:
    print(f"Error: {e}")

finally:
    connection.close()
    print('MySQL connection closed.')
