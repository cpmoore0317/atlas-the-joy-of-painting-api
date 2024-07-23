const mysql = require('mysql');
const fs = require('fs');

// Configuration for the MySQL connection
const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: 'root',
  multipleStatements: true
};

const connection = mysql.createConnection(dbConfig);

// Function to execute the SQL script
function runSqlScript() {
  const scriptFilePath = './sql/database_init.sql';
  fs.readFile(scriptFilePath, 'utf8', (err, sqlScript) => {
    if (err) {
      console.error('Error reading SQL script file:', err);
      return;
    }

    connection.query(sqlScript, (queryErr, results, fields) => {
      if (queryErr) {
        console.error('Error executing SQL script:', queryErr);
        return;
      }

      console.log('SQL script executed successfully.');

      // Close the database connection
      closeConnection();
    });
  });
}

// Function to close the MySQL connection
function closeConnection() {
  connection.end((endErr) => {
    if (endErr) {
      console.error('Error closing MySQL connection:', endErr);
    } else {
      console.log('MySQL connection closed.');
    }
  });
}

// Initialize the database connection and execute the SQL script
connection.connect((connErr) => {
  if (connErr) {
    console.error('Error connecting to MySQL:', connErr);
    return;
  }

  runSqlScript();
});
