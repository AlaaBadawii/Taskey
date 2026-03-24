import json
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, render_template, redirect, url_for, request, flash
from . import db
from flask_login import login_required, current_user
from .models.task import Task
from .models.group import Group
from .models.user import User
from datetime import date
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def parse_due_date(raw_due_date):
    if not raw_due_date:
        return None
    try:
        return date.fromisoformat(raw_due_date)
    except ValueError:
        return None


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


def build_task_summary(tasks):
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.status == 'completed')
    pending_tasks = total_tasks - completed_tasks
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }


def parse_task_steps(raw_steps):
    cleaned_steps = []
    for step in raw_steps:
        normalized_step = step.strip()
        if normalized_step:
            cleaned_steps.append(normalized_step)
    return cleaned_steps


def build_task_steps(step_texts, completed_states=None):
    completed_states = completed_states or []
    steps = []

    for index, step_text in enumerate(step_texts):
        normalized_step = step_text.strip()
        if not normalized_step:
            continue

        is_completed = False
        if index < len(completed_states):
            is_completed = completed_states[index] == 'true'

        steps.append({
            'text': normalized_step,
            'completed': is_completed,
        })

    return steps


def serialize_task_steps(steps):
    return json.dumps(steps) if steps else None


def deserialize_task_steps(raw_steps):
    if not raw_steps:
        return []

    try:
        parsed_steps = json.loads(raw_steps)
    except (TypeError, ValueError):
        parsed_steps = [raw_steps]

    if not isinstance(parsed_steps, list):
        return []

    normalized_steps = []
    for step in parsed_steps:
        if isinstance(step, str) and step.strip():
            normalized_steps.append({
                'text': step.strip(),
                'completed': False,
            })
        elif isinstance(step, dict):
            text = step.get('text', '').strip()
            if text:
                normalized_steps.append({
                    'text': text,
                    'completed': bool(step.get('completed', False)),
                })

    return normalized_steps


@main.route('/')
def index():
    return render_template('index.html', current_page='index')

@main.route('/profile')
@login_required
def profile():
    groups = Group.query.filter_by(user_id=current_user.id).all()

    today = date.today()
    tasks = Task.query.filter_by(user_id=current_user.id, due_date=today).all()
    task_summary = build_task_summary(tasks)
    return render_template('profile.html', current_page='profile', groups=groups, tasks=tasks, task_num=task_summary['total_tasks'], task_summary=task_summary)


@main.route('/profile/create', methods=['GET', 'POST'])
@login_required
def create():
    groups = Group.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        # Retrieve form data
        task_name = request.form.get('task_name')
        title = request.form.get('title')
        task_description = request.form.get('task_description')
        due_date = parse_due_date(request.form.get('due_date'))
        priority = request.form.get('priority', 'low')
        group_name = request.form.get('group_name')
        task_steps = build_task_steps(request.form.getlist('task_steps[]'))

        # Validate form data
        if not task_name or not due_date or not priority:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('main.create'))

        group = Group.query.filter_by(group_name=group_name, user_id=current_user.id).first()
        if group is None:
            group = Group(group_name=group_name, user_id=current_user.id)
            group.save()
        group_id = group.id
        
        new_task = Task(
            task_name=task_name,
            task_title=title,
            task_description=task_description,
            due_date=due_date,
            priority=priority,
            steps=serialize_task_steps(task_steps),
            group_id=group_id,
            user_id=current_user.id)

        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('main.upcoming'))

    return render_template('create.html', current_page='create', groups=groups)

@main.route('/profile/edit/<task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    groups = Group.query.filter_by(user_id=current_user.id).all()
    task = Task.query.get(task_id)

    if request.method == 'POST':
        task_name = request.form.get('task_name')
        task_title = request.form.get('task_title')
        due_date = parse_due_date(request.form.get('due_date'))
        priority = request.form.get('priority')
        group_id = request.form.get('group_id')
        task_description = request.form.get('task_description')
        task_steps = build_task_steps(
            request.form.getlist('task_steps[]'),
            request.form.getlist('task_steps_completed[]'),
        )

        # Validate form data
        if not task_name or not task_title or not due_date or not priority or not group_id:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('main.edit', task_id=task_id))

        group = Group.query.filter_by(id=group_id, user_id=current_user.id).first()
        if not group:
            flash('Please choose a valid group.', 'error')
            return redirect(url_for('main.edit', task_id=task_id))

        task.task_name = task_name
        task.task_title = task_title
        task.due_date = due_date
        task.priority = priority
        task.group_id = group.id
        task.task_description = task_description
        task.steps = serialize_task_steps(task_steps)

        db.session.commit()
        return redirect(url_for('main.task', task_id=task.id))

    group_name = Group.query.filter_by(id=task.group_id).first().group_name
    task_steps = deserialize_task_steps(task.steps)

    return render_template('edit.html', current_page='edit', task=task, group_name=group_name, groups=groups, task_steps=task_steps)

@main.route('/profile/delete/<task_id>')
@login_required
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.upcoming'))


@main.route('/profile/upcoming')
@login_required
def upcoming():
    groups = Group.query.filter_by(user_id=current_user.id).all()

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    task_summary = build_task_summary(tasks)
    return render_template('upcoming.html', tasks=tasks, current_page='upcoming', groups=groups, task_num=task_summary['total_tasks'], task_summary=task_summary)

@main.route('/profile/task/<task_id>')
@login_required
def task(task_id):
    groups = Group.query.filter_by(user_id=current_user.id).all()

    task = Task.query.get(task_id)
    group_name = Group.query.filter_by(id=task.group_id).first().group_name
    task_steps = deserialize_task_steps(task.steps)
    return render_template('task.html', current_page='task', task=task, group_name=group_name, groups=groups, task_steps=task_steps)

@main.route('/profile/task/<task_id>/steps', methods=['POST'])
@login_required
def save_task_steps(task_id):
    task = Task.query.get(task_id)
    if not task or task.user_id != current_user.id:
        flash('Task not found.', 'error')
        return redirect(url_for('main.profile'))

    task_steps = deserialize_task_steps(task.steps)
    completed_indices = set()

    for raw_index in request.form.getlist('completed_step_indices[]'):
        try:
            completed_indices.add(int(raw_index))
        except (TypeError, ValueError):
            continue

    for index, step in enumerate(task_steps):
        step['completed'] = index in completed_indices

    task.steps = serialize_task_steps(task_steps)
    db.session.commit()
    flash('Task steps saved successfully.')
    return redirect(url_for('main.task', task_id=task_id))


@main.route('/profile/task/<task_id>/step/<int:step_index>/toggle')
@login_required
def toggle_task_step(task_id, step_index):
    task = Task.query.get(task_id)
    if not task or task.user_id != current_user.id:
        flash('Task not found.', 'error')
        return redirect(url_for('main.profile'))

    task_steps = deserialize_task_steps(task.steps)
    if step_index < 0 or step_index >= len(task_steps):
        flash('Step not found.', 'error')
        return redirect(url_for('main.task', task_id=task_id))

    task_steps[step_index]['completed'] = not task_steps[step_index]['completed']
    task.steps = serialize_task_steps(task_steps)
    db.session.commit()

    return redirect(url_for('main.task', task_id=task_id))

@main.route('/profile/group/<group_id>')
@login_required
def group(group_id):
    groups = Group.query.filter_by(user_id=current_user.id).all()

    group = Group.query.get(group_id)
    group_name = Group.query.filter_by(id=group_id).first().group_name

    current_page = group.id
    tasks = Task.query.filter_by(group_id=group_id).all()
    task_summary = build_task_summary(tasks)
    return render_template('group.html', tasks=tasks, current_page=current_page, groups=groups, task_num=task_summary['total_tasks'], task_summary=task_summary, group_name=group_name)

# @main.route('/profile/group/delete/<group_id>')
# def delete_group(group_id):
#     groups = Group.query.filter_by(user_id=current_user.id).all()

#     group = Group.query.get(group_id)
#     tasks = Task.query.filter_by(group_id=group_id).all()
#     for task in tasks:
#         db.session.delete(task)
#     db.session.delete(group)
#     db.session.commit()
#     return redirect(url_for('main.profile'), current_page='profile', groups=groups)

@main.route('/profile/start')
@login_required
def start():
    groups = Group.query.filter_by(user_id=current_user.id).all()

    return render_template('start.html', current_page='start', groups=groups)


@main.route('/profile/complete/<task_id>')
@login_required
def complete(task_id):
    task = Task.query.get(task_id)
    if task.status == 'completed':
        task.status = 'pending'
    else:
        task.status = 'completed'
    db.session.commit()
    return redirect(url_for('main.profile'))


@main.route('/profile/settings')
@login_required
def settings():
    groups = Group.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'settings.html',
        current_page='settings',
        groups=groups,
    )


@main.route('/profile/settings/preferences', methods=['POST'])
@login_required
def update_preferences():
    theme = request.form.get('theme', 'light')
    if theme not in {'light', 'dark'}:
        flash('Please choose a valid theme.')
        return redirect(url_for('main.settings'))

    current_user.theme = theme
    db.session.commit()
    flash('Preferences updated successfully.')
    return redirect(url_for('main.settings'))


@main.route('/profile/settings/password', methods=['POST'])
@login_required
def update_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not current_user.check_password(current_password):
        flash('Your current password is incorrect.')
        return redirect(url_for('main.settings'))

    if len(new_password) < 8:
        flash('Your new password must be at least 8 characters long.')
        return redirect(url_for('main.settings'))

    if new_password != confirm_password:
        flash('New passwords do not match.')
        return redirect(url_for('main.settings'))

    current_user.set_password(new_password)
    db.session.commit()
    flash('Password updated successfully.')
    return redirect(url_for('main.settings'))


@main.route('/profile/settings/photo', methods=['POST'])
@login_required
def update_profile_photo():
    photo = request.files.get('profile_image')
    image_path = save_profile_image(photo)

    if not image_path:
        flash('Please upload a valid image file: png, jpg, jpeg, gif, or webp.')
        return redirect(url_for('main.settings'))

    old_image = current_user.profile_image
    current_user.profile_image = image_path
    db.session.commit()
    if old_image and old_image != image_path:
        delete_profile_image(old_image)
    flash('Profile picture updated successfully.')
    return redirect(url_for('main.settings'))
