const mysql = require('mysql');
const fs = require('fs');
const path = require('path');

const colors_used = path.join(__dirname, 'data', 'The Joy Of Painting - Colors Used.csv');
const episode_dates = path.join(__dirname, 'data', 'The Joy Of Painting - Subject Matter.txt');
const subject_matter = path.join(__dirname, 'data', 'The Joy Of Painting - Episode Dates.txt');

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'root',
  database: 'joy_of_painting',
  multipleStatements: true
});

// Read colors used for episodes table
function colorsUsedforEpisodes() {
  return new Promise((resolve, reject) => {
    fs.readFile(colors_used, 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading colors used file:', err);
        reject(err);
        return;
      }
      // Parse the CSV data and extract rows
      const rows = data.trim().split('\n').map(row => row.split(','));
      let episodes = [];
      for (let i = 1; i < rows.length; i++) {
        episodes.push([rows[i][3], rows[i][4], rows[i][5], rows[i][2], rows[i][7]]);
      }
      resolve(episodes);
    });
  });
};

function datesForEpisodes() {
  return new Promise((resolve, reject) => {
    fs.readFile(episode_dates, 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading episode dates file:', err);
        reject(err);
        return;
      }
      // Parse the text data and extract rows
      const rows = data.trim().split('\n').map(row => row.split('('));
      let dates = [];
      for (let i = 0; i < rows.length; i++) {
        let item_date = new Date(rows[i][1].split(')')[0]);
        item_date = item_date.toLocaleDateString();
        dates.push(item_date.toString());
      }
      resolve(dates);
    });
  });
}

function mergeData(data1, data2) {
  for (let i = 0; i < data1.length; i++) {
    data1[i].push(data2[i]);
  }
  return data1;
}

// Call the functions to read and merge data from files
Promise.all([colorsUsedforEpisodes(), datesForEpisodes()])
  .then(([colors_data, dates_data]) => {
    const mergedData = mergeData(colors_data, dates_data);
    console.log(mergedData[mergedData.length - 3]);
    const sql = "INSERT INTO episodes (title, season_number, episode_number, painting_img_src, painting_yt_src, air_date) VALUES ?";

    connection.query(sql, [mergedData], (err, results, fields) => {
      if (err) {
        console.error('Error inserting data into episodes table:', err);
        return;
      }
      console.log('Data inserted successfully into episodes table.');
    });
  })
  .catch((err) => {
    console.error('Error:', err);
  })
  .finally(() => {
    // Close the database connection
    connection.end((endErr) => {
      if (endErr) {
        console.error('Error closing MySQL connection:', endErr);
      } else {
        console.log('MySQL connection closed.');
      }
    });
  });
