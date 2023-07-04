# Task Manager

# Task Manager Application

This is a Task Manager application built with Django and Django REST Framework. The application allows users to create tasks and subtasks, and manage them via a REST API. User authentication is based on token authentication another project of mine [UserAPI](https://github.com/MastersMasterM/UserAPI/)

The application consists of four main components:

1. User: A separate project that handles user authentication based on token authentication.

2. Core: All the models are defined in this app

2. Taskmanager: The main project that provides the REST API for creating and managing tasks and subtasks.

3. UI: An app that renders HTML pages and makes appropriate HTTP requests to the Taskmanager endpoints.

## Installation

To run the Task Manager application, you need to have Docker installed on your system. Once you have Docker installed, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/MastersMasterM/TaskManager.git
```

2. Change into the cloned directory:

```bash
cd TaskManager
```

3. Build the Docker image:

```bash
docker-compose build
```

4. Start the Docker containers:

```bash
docker-compose up
```

5. Access the application in your browser:

```bash
http://localhost:8000/
```

## Usage

The Task Manager application provides a REST API for creating and managing tasks and subtasks. The API endpoints are documented using SwaggerUI, which can be accessed at:

```bash
http://localhost:8000/api/docs/
```

The UI app allows users to interact with the Task Manager application via a web interface. To access the UI, go to:

```bash
http://localhost:8000/
```

The UI app provides the following features:

- Create new tasks
- Create subtasks for existing tasks
- View all tasks and their subtasks
- Mark tasks as complete
- Delete tasks and subtasks

## Future Features

In the future, we plan to add the following features to the Task Manager application:

- Project concept: Allow users to group tasks into projects
- Task assignment: Allow users to assign tasks to other users
- Task priority: Allow users to set task priorities
- Project Management Concept

## Contributing

If you'd like to contribute to the Task Manager application, please fork the repository and create a pull request. I welcome all contributions!

## License

The Task Manager application is distributed under the MIT License. See `LICENSE` for more information.