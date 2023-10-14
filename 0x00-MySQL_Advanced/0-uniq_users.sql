-- Task: Create the 'users' table if it does not exist
-- Attributes: id, email, and name
CREATE TABLE IF NOT EXISTS users (
  id INT AUTOINCREMENT NOT NULL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255)
);
