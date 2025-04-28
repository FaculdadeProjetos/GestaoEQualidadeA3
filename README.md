# User and Irrigation Management System

A Python Flask application with MySQL database for user management and automated irrigation control, built with Docker.

## Features

- User Authentication (Login/Register)
- User Management (CRUD operations)
- Irrigation System Management
  - Monitor soil moisture levels
  - Track irrigation history
  - Activate/deactivate controllers
  - Manual irrigation control
- Containerized with Docker

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Start the application with Docker Compose:
   ```
   docker-compose up -d
   ```

3. Access the application in your browser:
   ```
   http://localhost:5000
   ```

## Troubleshooting

### Import Error
If you encounter the error `Could not import 'app.app'`, ensure:
1. The `FLASK_APP` environment variable in `docker-compose.yml` is set to `wsgi.py`
2. The volume mapping in `docker-compose.yml` is correctly configured
3. The Dockerfile has `ENV FLASK_APP=wsgi.py` specified
4. You have the `wsgi.py` file in your project root

### Circular Import Error
If you encounter a circular import error (like `ImportError: cannot import name 'create_app' from partially initialized module 'app'`):
1. Make sure not to name files that could conflict with directory names (e.g., don't have both `app.py` and `app/` directory)
2. Check that your Docker volume mappings keep file structures separate
3. Ensure the correct `PYTHONPATH` is set in your Dockerfile

If problems persist, you can run the application locally with:
```
python run.py
```

## Project Structure

- `app/`: The Flask application
  - `__init__.py`: Application factory and configuration
  - `models.py`: Database models
  - `auth.py`: Authentication routes and forms
  - `users.py`: User management routes and forms
  - `irrigation.py`: Irrigation system management routes and forms
  - `templates/`: HTML templates
- `Dockerfile`: Docker configuration for the Python application
- `docker-compose.yml`: Docker Compose configuration
- `requirements.txt`: Python dependencies

## Default Credentials

On first run, you'll need to register a new user.

## Environment Variables

The following environment variables can be set in the `docker-compose.yml` file:

- `FLASK_APP`: The path to the Flask application
- `FLASK_DEBUG`: Set to 1 for development mode
- `DATABASE_URL`: The MySQL connection URL
- `SECRET_KEY`: Secret key for session encryption (change for production)

## Development

To run the application in development mode:

```
docker-compose up
```

## License

MIT 