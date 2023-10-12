-- Task: Create the 'users' table if it does not exist

CREATE TABLE IF NOT EXISTS users (
  id INT AUTOINCREMENT NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  PRIMARY KEY (id)
);
