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
    return render_template('profile.html', current_page='profile')


@main.route('/profile/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Retrieve form data
        task_name = request.form.get('task_name')
        title = request.form.get('title')
        task_description = request.form.get('task_description')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')
        group_name = request.form.get('group_name')

        # Validate form data
        if not task_name or not due_date or not priority:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('main.create'))

        group = Group.query.filter_by(group_name=group_name).first()
        if group is None:
            group = Group(group_name=group_name)
            group.save()
        group_id = group.id
        
        new_task = Task(
            task_name=task_name,
            task_title=title,
            task_description=task_description,
            due_date=due_date,
            priority=priority,
            group_id=group_id,
            user_id=current_user.id)

        db.session.add(new_task)
        db.session.commit()
        flash('Task created successfully' , 'success')
        return redirect(url_for('main.profile'), current_page='profile')

    return render_template('create.html', current_page='create')

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

        db.session.commit()
        return redirect(url_for('main.home'), current_page='main')

    return render_template('edit.html', current_page='edit')

@main.route('/profile/upcoming')
def upcoming():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('upcoming.html', tasks=tasks, current_page='upcoming')

@main.route('/profile/delete')
def delete():
    name=current_user.username
    redirect(url_for('main.profile'))
    flash('Task Deleted')
    return render_template('profile.html', name=name)

@main.route('/profile/task/<task_id>')
def task(task_id):
    task = Task.query.get(task_id)
    group_name = Group.query.filter_by(id=task.group_id).first().group_name
    return render_template('task.html', current_page='task', task=task, group_name=group_name)

# @main.route('/profile/settings')
# def settings():
#     return render_template('settings.html', name=current_user.username)

