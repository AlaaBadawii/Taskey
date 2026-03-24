import os
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

db = SQLAlchemy()


def ensure_user_settings_columns():
    inspector = inspect(db.engine)
    if 'user' not in inspector.get_table_names():
        return

    user_columns = {column['name'] for column in inspector.get_columns('user')}

    if 'theme' not in user_columns:
        db.session.execute(
            text("ALTER TABLE user ADD COLUMN theme VARCHAR(20) NOT NULL DEFAULT 'light'")
        )

    if 'profile_image' not in user_columns:
        db.session.execute(
            text("ALTER TABLE user ADD COLUMN profile_image VARCHAR(255)")
        )

    db.session.commit()

def create_app():
    app = Flask(__name__)

    # Retrieve configuration from environment variables
    secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
    database_url = os.getenv('DATABASE_URL')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')

    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    elif all([db_user, db_password, db_host, db_name]):
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f'mysql+mysqldb://{db_user}:{db_password}@{db_host}/{db_name}'
        )
    else:
        sqlite_path = Path(app.instance_path) / 'taskey.db'
        sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{sqlite_path}'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint for any other routes in our app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()
        ensure_user_settings_columns()

    return app
