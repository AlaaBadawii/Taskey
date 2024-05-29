from . import create_app, db
from .models.user import User
from .models.task import Task
from .models.group import Group
from .models.tag import Tag

# Create the Flask application instance
app = create_app()


# Use the application context
with app.app_context():
    print("Creating all tables...")
    db.create_all()
    print('tables created')
    db.session.commit()

