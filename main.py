from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from flask_login import login_required, current_user
from .models.task import Task
from .models.group import Group

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.username)


@main.route('/profile/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Retrieve form data
        task_name = request.form.get('task_name')
        title = request.form.get('title')
        descrition = request.form.get('descrition')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')
        group = request.form.get('group')

        # Validate form data
        if not task_name or not due_date or not priority:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('main.create'))

        # Create a new task
        try:
            groub_id = Group.query.filter_by(group_name=group).first().id
            new_task = Task(
                task_name=task_name,
                due_date=due_date,
                priority=priority,
                title=title,
                descrition=descrition,
                group_id=groub_id,
                user_id=current_user.id)

            db.session.add(new_task)
            db.session.commit()
            flash('Task created successfully', 'success')
            return redirect(url_for('main.home'))  # Redirect to home page after task creation
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the task. Please try again.', 'error')
            return redirect(url_for('main.create'))

    return render_template('create.html')

@main.route('/profile/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        task_id = request.form.get('task_id')
        task_name = request.form.get('task_name')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')
        group = request.form.get('group')

        # Validate form data
        if not task_name or not due_date or not priority:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('main.edit'))

        task = Task.query.get(task_id)
        task.task_name = task_name
        task.due_date = due_date
        task.priority = priority
        task.group_name = group

        try:
            db.session.commit()
            flash('Task updated successfully', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the task. Please try again.', 'error')
            return redirect(url_for('main.edit'))

    return render_template('edit_task.html')
# @main.route('/profile/delete')
# def delete():
#     name=current_user.username
#     redirect(url_for('main.profile'))
#     flash('Task Deleted')

# @main.route('/profile/tasks')
# def tasks():
#     return render_template('tasks.html', name=current_user.username)

# @main.route('/profile/settings')
# def settings():
#     return render_template('settings.html', name=current_user.username)