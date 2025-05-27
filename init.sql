-- Initialization script for the database
CREATE DATABASE IF NOT EXISTS user_management;

USE user_management;

GRANT ALL PRIVILEGES ON user_management.* TO 'user'@'%';
FLUSH PRIVILEGES; 