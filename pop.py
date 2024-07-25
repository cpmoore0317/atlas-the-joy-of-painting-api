import pymysql
import pandas as pd
from datetime import datetime

# Configuration for the MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'joy_of_painting',
    'autocommit': True
}

colors_used = './data/The Joy Of Painiting - Colors Used'
episode_dates = './data/The Joy Of Painiting - Subject Matter'
subject_matter = './data/The Joy Of Painting - Episode Dates'

def read_colors_used():
    df = pd.read_csv(colors_used)
    return df[['Column3', 'Column4', 'Column5', 'Column2', 'Column7']].values.tolist()

def read_episode_dates():
    with open(episode_dates, 'r', encoding='utf8') as file:
        data = file.readlines()

    dates = []
    for row in data:
        try:
            date_str = row.split('(')[1].split(')')[0]
            date = datetime.strptime(date_str, '%B %d, %Y').strftime('%Y-%m-%d')
            dates.append(date)
        except Exception as e:
            print(f'Error processing row: {row}, {e}')
            dates.append(None)

    return dates

def merge_data(data1, data2):
    return [row + [data2[idx]] for idx, row in enumerate(data1)]

def insert_data(data):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    sql = """
        INSERT INTO episodes (title, season_number, episode_number, painting_img_src, painting_yt_src, air_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(sql, data)
        print('Data inserted successfully into episodes table.')
    except Exception as e:
        print(f'Error inserting data into episodes table: {e}')
    finally:
        cursor.close()
        connection.close()
        print('MySQL connection closed.')

# Call the functions to read and merge data from files
if __name__ == "__main__":
    try:
        colors_data = read_colors_used()
        dates_data = read_episode_dates()
        merged_data = merge_data(colors_data, dates_data)
        insert_data(merged_data)
    except Exception as e:
        print(f'Error: {e}')
