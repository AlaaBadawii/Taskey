# Taskey

Taskey is a Flask task management app for organizing daily work with groups, priorities, due dates, and a cleaner dashboard experience.

## What's New

- Refreshed UI across the dashboard, task views, and forms
- New settings page for theme selection, password changes, and profile photo uploads
- Dark mode support stored per user
- Task steps/checklists with saved progress
- Better task summary cards for Today, Upcoming, and Group views
- Automatic database setup on startup
- SQLite fallback for local development, with optional MySQL or `DATABASE_URL`
- Safer account deletion that also removes uploaded profile photos

## Features

- User signup, login, logout, and account deletion
- Create, edit, complete, and delete tasks
- Organize tasks into groups
- Set due dates, priorities, descriptions, and multi-step checklists
- Track task counts for total, completed, and pending work
- Upload a profile picture
- Switch between light and dark theme
- Responsive navigation for desktop and mobile

## Tech Stack

- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLAlchemy
- Jinja2
- Vanilla JavaScript
- MySQL or SQLite

## Installation

### Prerequisites

- Python 3.8+
- `pip`
- MySQL only if you want to use MySQL instead of the built-in SQLite fallback

### Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/AlaaBadawii/Taskey
   cd taskey
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

   On Windows:

   ```sh
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Configure environment variables.

   Minimum:

   ```sh
   export SECRET_KEY=your-secret-key
   ```

   Optional database configuration:

   ```sh
   export DATABASE_URL=sqlite:////absolute/path/to/taskey.db
   ```

   Or use MySQL:

   ```sh
   export DB_USER=your-db-username
   export DB_PASSWORD=your-db-password
   export DB_HOST=localhost
   export DB_NAME=taskey_db
   ```

   If no database settings are provided, Taskey will create and use a local SQLite database at `instance/taskey.db`.

5. If you are using MySQL, create the database first:

   ```sql
   CREATE DATABASE taskey_db;
   ```

6. Start the app:

   From inside the `taskey/` project directory:

   ```sh
   python3 app.py
   ```

   Or run it with Flask from the parent directory of `taskey/`:

   ```sh
   cd ..
   flask --app taskey:create_app run --debug
   ```

   If you stay inside the `taskey/` directory and want to use Flask directly, set the parent directory on `PYTHONPATH` first:

   ```sh
   PYTHONPATH=.. flask --app taskey:create_app run --debug
   ```

   Note:

   - `python3 app.py` works when you are inside the project folder.
   - `flask --app taskey:create_app run` works when you are in the parent folder of `taskey/`.

7. Open the app at `http://127.0.0.1:5000`.

## Database Notes

- Tables are created automatically when the app starts.
- User settings columns such as `theme` and `profile_image` are added automatically if they do not already exist.
- `create.py` is still available if you want to trigger table creation manually:

  ```sh
  python -m taskey.create
  ```

## Usage

After signing up and logging in, you can:

1. Create tasks with a name, title, description, due date, priority, and group.
2. Add checklist steps to a task during creation or editing.
3. Track tasks from Today, Upcoming, and Group pages.
4. Open a task detail page and save checklist progress.
5. Change your password, theme, and profile photo from Settings.

## Project Structure

```text
taskey/
├── app.py
├── __init__.py
├── auth.py
├── main.py
├── create.py
├── models/
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
└── templates/
```

## Configuration

Supported environment variables:

- `SECRET_KEY`
- `DATABASE_URL`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_NAME`

## Notes

- Profile images are stored under `static/uploads/profile_pictures/`.
- Allowed profile image formats are `png`, `jpg`, `jpeg`, `gif`, and `webp`.
- The current default local database path is `instance/taskey.db`.
