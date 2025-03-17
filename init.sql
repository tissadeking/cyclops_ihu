
-- drop previous database and tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS data_store;
DROP DATABASE IF EXISTS cyclops;

-- Create the database if it doesn't exist
CREATE DATABASE cyclops;

-- Use the cyclops database
USE cyclops;

-- Create the users table if it doesn't exist
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    userid VARCHAR(60) UNIQUE NOT NULL
);


-- Create the data_store table if it doesn't exist
CREATE TABLE data_store (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    userid VARCHAR(60) NOT NULL,
    intent_id VARCHAR(30) NOT NULL,
    data LONGTEXT NOT NULL,
    data_description TEXT NOT NULL
);

