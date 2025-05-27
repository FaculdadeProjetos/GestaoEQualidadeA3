-- Initialization script for the database
-- This script will be executed when the MySQL container starts for the first time

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS user_management;

-- Use the database
USE user_management;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON user_management.* TO 'user'@'%';
FLUSH PRIVILEGES; 