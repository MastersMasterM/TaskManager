# UserAPI

UserAPI is a RESTful API built with Django, Django Rest Framework, and Postgres that allows users to create and manage their profiles using token authentication.
This project is based on Dockerized Django and Postgres Starterkit [https://github.com/MastersMasterM/Django-Postgres-Imp4Docker/tree/main]

## Features

- User authentication using token authentication
- Create user profiles using email address as primary key
- Manage user profiles by changing name and password
- Store user data securely in Postgres database
- Containerized using Docker for easy deployment
- API documentation using Swagger UI

## Requirements

- Docker
- Docker Compose

## Installation and Usage

1. Clone the repository:

```
git clone https://github.com/MastersMasterM/recipe-app-api.git
```

2. Build and run the Docker containers:

```
docker-compose up --build
```

3. Access the API documentation at http://localhost:8000/api/docs/

4. Use Swagger UI to explore and test the API endpoints.

## API Endpoints

- `POST /api/user/create/` - Create a new user profile
- `POST /api/user/token/` - Create a new token for the user profile
- `GET /api/user/me/` - Get user profile information (email and name)
- `PUT /api/user/me/` - Update user profile information (name and password)
- `PATCH /api/user/me/` - Update part of the user profile information (name or password)

## Authentication

To authenticate with the API, include an `Authorization` header in your requests with a token in the format `Token <token>` where `<token>` is the user's authentication token.

## Testing

To run the automated tests, use the following command:

```
docker-compose run app sh -c "python manage.py test && flake8"
```

## License

UserAPI is released under the MIT License. See [LICENSE](LICENSE) for details.
