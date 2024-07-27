import pymysql
import csv
import os

# Configuration for the MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'joy_of_painting'
}

# File paths
colors_used_file = './data/The Joy Of Painting - Colors Used'
subject_matter_file = './data/The Joy Of Painting - Subject Matter'
episode_dates_file = './data/The Joy Of Painting - Episode Dates'

# Create a MySQL connection
try:
    connection = pymysql.connect(**db_config)
except pymysql.MySQLError as e:
    print(f"Error connecting to MySQL: {e}")
    raise

def read_csv_file(filename, columns=None):
    data = []
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        if columns is None:
            columns = [f"Column{i}" for i in range(len(next(reader)))]
            file.seek(0)  # Go back to the start of the file
        for row in reader:
            if len(row) == len(columns):  # Ensure row matches expected column length
                data.append(dict(zip(columns, row)))
    return data

def colors_used_for_episodes():
    columns = ['painting_title', 'season', 'episode', 'img_src', 'youtube_src', 'colors', 'color_hex']
    return read_csv_file(colors_used_file, columns)

def subject_matters_for_episodes():
    columns = ['EPISODE']  # Adjust if needed
    return read_csv_file(subject_matter_file, columns)

def episode_dates():
    columns = ['Title', 'Date']
    return read_csv_file(episode_dates_file, columns)

def insert_data():
    colors_data = colors_used_for_episodes()
    subject_matters_data = subject_matters_for_episodes()
    dates_data = episode_dates()

    try:
        # Insert into episodes table
        episode_sql = """
        INSERT INTO episodes (title, season_number, episode_number, painting_img_src, painting_yt_src, air_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            for row in colors_data:
                title = row['painting_title']
                season = int(row['season'])
                episode = int(row['episode'])
                img_src = row['img_src']
                youtube_src = row['youtube_src']
                air_date = next((date['Date'] for date in dates_data if date['Title'].strip() == title), None)
                cursor.execute(episode_sql, (title, season, episode, img_src, youtube_src, air_date))

        # Insert into colors table
        color_sql = "INSERT INTO colors (color_name, color_hex) VALUES (%s, %s)"
        with connection.cursor() as cursor:
            color_names_hex = [(row['colors'], row['color_hex']) for row in colors_data]
            for color, hex in color_names_hex:
                cursor.execute(color_sql, (color, hex))

        # Insert into episode_colors table
        episode_colors_sql = """
        INSERT INTO episode_colors (episode_id, color_id)
        SELECT e.episode_id, c.color_id
        FROM episodes e, colors c
        WHERE e.title = %s AND c.color_name = %s
        """
        with connection.cursor() as cursor:
            for row in colors_data:
                title = row['painting_title']
                colors = row['colors'].split(';')  # Assuming colors are separated by semicolons
                for color in colors:
                    cursor.execute(episode_colors_sql, (title, color))

        # Insert into subject_matters table
        subject_matters = set()
        for row in subject_matters_data:
            subjects = row['EPISODE'].split(';')  # Adjust if needed
            subject_matters.update(subjects)

        subject_sql = "INSERT INTO subject_matters (subject_matter_name) VALUES (%s)"
        with connection.cursor() as cursor:
            for subject in subject_matters:
                cursor.execute(subject_sql, (subject,))

        # Insert into episode_subject_matters table
        episode_subject_matters_sql = """
        INSERT INTO episode_subject_matters (episode_id, subject_matter_id)
        SELECT e.episode_id, sm.subject_matter_id
        FROM episodes e, subject_matters sm
        WHERE e.title = %s AND sm.subject_matter_name = %s
        """
        with connection.cursor() as cursor:
            for row in subject_matters_data:
                title = row['EPISODE']
                subjects = row['EPISODE'].split(';')  # Adjust if needed
                for subject in subjects:
                    cursor.execute(episode_subject_matters_sql, (title, subject))

        connection.commit()
        print('Data inserted successfully into all tables.')

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()
        print('MySQL connection closed.')

# Run the insertion process
if __name__ == "__main__":
    insert_data()
