-- Create the database
CREATE DATABASE if not exists jecnabot;

USE jecnabot;

-- Create user 
create user 'Faltin'@'localhost' identified by 'Faltin';

-- Grant user with all privileges for this database
GRANT ALL PRIVILEGES ON jecnabot.* TO 'Faltin'@'localhost';
FLUSH PRIVILEGES;

-- Create the `users` table
CREATE TABLE if not exists users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the `sessions` table
CREATE TABLE if not exists `sessions` (
    id CHAR(36) PRIMARY KEY, -- Use UUID for unique session IDs
    user_id INT NOT NULL,
    session_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create the `messages` table
CREATE TABLE if not exists messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id CHAR(36) NOT NULL,
    content TEXT NOT NULL,
    is_question BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);