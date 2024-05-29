# Taskey

Taskey is a task management application designed to help users organize their tasks efficiently. Built with Flask, SQLAlchemy, and Flask-Login, Taskey provides a simple and intuitive interface for managing daily tasks.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration](#configuration)

## Features

- User authentication and authorization
- Create, read, update, and delete tasks
- Organize tasks by categories
- Set due dates and priorities for tasks
- Responsive design for mobile and desktop use

## Installation

### Prerequisites

- Python 3.8+
- MySQL

### Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/AlaaBadawii/Taskey
    cd taskey
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.env` file in the root directory of your project and add the following:

    ```sh
    SECRET_KEY=your-secret-key
    DB_USER=your-db-username
    DB_PASSWORD=your-db-password
    DB_HOST=localhost
    DB_NAME=taskey_db
    ```

    or just before running the program:
     ```sh
    export SECRET_KEY=your-secret-key
    export DB_USER=your-db-username
    export DB_PASSWORD=your-db-password
    export DB_HOST=localhost
    export DB_NAME=taskey_db
    ```

5. **Set up the database:**

    Log in to your MySQL server and create the database:

    ```sql
    CREATE DATABASE taskey_db;
    ```

6. **Run the application:**

    ```sh
    cd ../
    flask --app=taskey --debug  run
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Usage

Once the application is running, you can:

1. **Register a new account** or **log in** with an existing account.
2. **Create new tasks** and organize them into categories.
3. **Edit or delete tasks** as needed.
4. **View tasks** in a prioritized list or by due date.

## Configuration

The application configuration is managed through environment variables. Ensure that you have all necessary variables set in your environment or in a `.env` file as described in the installation section.
