from pathlib import Path
from uuid import uuid4

from flask import current_app
from flask_login import current_user
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def save_profile_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None

    if not allowed_image(file_storage.filename):
        return None

    original_name = secure_filename(file_storage.filename)
    extension = original_name.rsplit('.', 1)[1].lower()
    filename = f'{current_user.id}_{uuid4().hex}.{extension}'

    upload_dir = Path(current_app.static_folder) / 'uploads' / 'profile_pictures'
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_storage.save(upload_dir / filename)
    return f'uploads/profile_pictures/{filename}'


def delete_profile_image(image_path):
    if not image_path:
        return

    image_file = Path(current_app.static_folder) / image_path
    if image_file.exists():
        image_file.unlink()
