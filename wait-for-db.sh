#!/bin/bash
set -e

echo "Waiting for MySQL to be ready..."
maxTries=60
while [ "$maxTries" -gt 0 ]; do
    echo "Attempting to connect to MySQL server ($maxTries attempts left)..."
    if python -c "import pymysql; pymysql.connect(host='db', user='user', password='password', database='user_management', port=3306)" &> /dev/null; then
        echo "MySQL is up and running!"
        break
    fi
    maxTries=$((maxTries-1))
    sleep 1
done

if [ "$maxTries" -le 0 ]; then
    echo "Could not connect to MySQL after multiple attempts. Exiting..."
    exit 1
fi

# Start the Flask application
exec "$@" 