# Chess Tournament Management System

A backend system for managing chess tournaments, built with Django and Django REST Framework. This system includes user authentication, player management, tournament management, match management, leaderboards, and caching using Redis.

## Features

- **User Authentication and Authorization**: User registration, login, and JWT-based authentication. Differentiates between regular users and admin users.
- **Player Management**: Admins can add, update, delete, and view player information, including name, age, rating, and country.
- **Tournament Management**: Admins can create tournaments with unique names, specific start and end dates, and assign players to tournaments.
- **Match Management**: Automatically generate pairings for each round based on Swiss-system tournament rules, and allow admins to update match results.
- **Leaderboard**: Generate and display a leaderboard for each tournament showing player ranks, points, and other relevant statistics.
- **Caching**: Use Redis for caching frequently accessed data to improve performance.

## Requirements

- Python 3.7+
- Django 3.2+
- Django REST Framework
- Redis

## Installation

1. **Clone the repository**:
    ```bash
    git clone git@github.com:MIRZAYEV07/ChessTournament.git
    cd chess-tournament-management
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Redis**:
    - Install Redis on your system. Refer to the [official Redis installation guide](https://redis.io/download).
    - Start the Redis server:
        ```bash
        redis-server
        ```

5. **Configure the database and cache settings**:
    - Update `settings.py` with your database configuration.
    - Ensure the cache settings in `settings.py` are configured to use Redis:
        ```python
        CACHES = {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': 'redis://127.0.0.1:6379/1',
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                },
            }
        }
        ```

6. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

7. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

8. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the admin interface at `http://127.0.0.1:8000/admin/` to manage users, players, tournaments, and matches.
- Use the API endpoints for managing tournaments, players, and matches. The API documentation is available at `http://127.0.0.1:8000/swagger/`.

## API Endpoints

- **Authentication**:
    - `POST /api/auth/register/`: Register a new user.
    - `POST /api/auth/login/`: Login and obtain a JWT token.

- **Players**:
    - `GET /api/players/`: List all players.
    - `POST /api/players/`: Create a new player (admin only).
    - `GET /api/players/{id}/`: Retrieve a player.
    - `PUT /api/players/{id}/`: Update a player (admin only).
    - `DELETE /api/players/{id}/`: Delete a player (admin only).

- **Tournaments**:
    - `GET /api/tournaments/`: List all tournaments.
    - `POST /api/tournaments/`: Create a new tournament (admin only).
    - `GET /api/tournaments/{id}/`: Retrieve a tournament.
    - `PUT /api/tournaments/{id}/`: Update a tournament (admin only).
    - `DELETE /api/tournaments/{id}/`: Delete a tournament (admin only).
    - `GET /api/tournaments/{id}/leaderboard/`: Get the leaderboard for a tournament.

- **Matches**:
    - `GET /api/matches/`: List all matches.
    - `POST /api/matches/`: Create a new match (admin only).
    - `GET /api/matches/{id}/`: Retrieve a match.
    - `PUT /api/matches/{id}/`: Update a match (admin only).
    - `DELETE /api/matches/{id}/`: Delete a match (admin only).
    - `POST /api/matches/generate_pairings/`: Generate pairings for a tournament round (admin only).

## Running Tests

The project includes unit tests, integration tests, and end-to-end tests.

1. **Run all tests**:
    ```bash
    pytest
    ```



