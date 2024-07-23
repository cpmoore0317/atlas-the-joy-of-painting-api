CREATE DATABASE IF NOT EXISTS joy_of_painting;
USE joy_of_painting;

-- Create table for episodes
CREATE TABLE IF NOT EXISTS episodes (
    episode_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    air_date DATE NOT NULL,
    episode_number INT NOT NULL,
    season_number INT NOT NULL,
    painting_img_src VARCHAR(255) NOT NULL,
    painting_yt_src VARCHAR(255) NOT NULL,
    UNIQUE (episode_number, season_number)
);

-- Create table for colors
CREATE TABLE IF NOT EXISTS colors (
    color_id INT PRIMARY KEY AUTO_INCREMENT,
    color_name VARCHAR(255) NOT NULL,
    color_hex VARCHAR(7) NOT NULL,
    UNIQUE (color_name, color_hex)
);

-- Create table for subject matters
CREATE TABLE IF NOT EXISTS subject_matters (
    subject_matter_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_matter_name VARCHAR(255) NOT NULL,
    UNIQUE (subject_matter_name)
);

-- Create join table for episodes and colors
CREATE TABLE IF NOT EXISTS episode_colors (
    episode_color_id INT PRIMARY KEY AUTO_INCREMENT,
    episode_id INT NOT NULL,
    color_id INT NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episodes(episode_id) ON DELETE CASCADE,
    FOREIGN KEY (color_id) REFERENCES colors(color_id) ON DELETE CASCADE,
    UNIQUE (episode_id, color_id)
);

-- Create join table for episodes and subject matters
CREATE TABLE IF NOT EXISTS episode_subject_matters (
    episode_subject_matter_id INT PRIMARY KEY AUTO_INCREMENT,
    episode_id INT NOT NULL,
    subject_matter_id INT NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episodes(episode_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_matter_id) REFERENCES subject_matters(subject_matter_id) ON DELETE CASCADE,
    UNIQUE (episode_id, subject_matter_id)
);
