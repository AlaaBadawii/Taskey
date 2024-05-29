from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from flask_login import login_required, current_user
from .models.task import Task
from .models.group import Group
from datetime import date
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    groups = Group.query.filter_by(user_id=current_user.id).all()

    today = date.today()
    tasks = Task.query.filter_by(user_id=current_user.id, due_date=today).all()
    task_num = len(tasks)
    return render_template('profile.html', current_page='profile', groups=groups, tasks=tasks, task_num=task_num)


@main.route('/profile/create', methods=['GET', 'POST'])
def create():
    groups = Group.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        # Retrieve form data
        task_name = request.form.get('task_name')
        title = request.form.get('title')
        task_description = request.form.get('task_description')
        due_date = request.form.get('due_date', date.today())
        priority = request.form.get('priority', 'low')
        group_name = request.form.get('group_name')

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
            group_id=group_id,
            user_id=current_user.id)

        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('main.upcoming'))

    return render_template('create.html', current_page='create', groups=groups)

@main.route('/profile/edit/<task_id>', methods=['GET', 'POST'])
def edit(task_id):
    groups = Group.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        task_id = task_id
        task_name = request.form.get('task_name')
        task_title = request.form.get('task_title')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')
        group = request.form.get('group')
        task_description = request.form.get('task_description')

        # Validate form data
        if not task_name or not due_date or not priority:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('main.edit'))

        task = Task.query.get(task_id)
        task.task_name = task_name
        task.task_title = task_title
        task.due_date = due_date
        task.priority = priority
        task.group_name = group
        task.task_description = task_description

        db.session.commit()
        return redirect(url_for('main.upcoming'))
    
    task = Task.query.get(task_id)
    group_name = Group.query.filter_by(id=task.group_id).first().group_name

    return render_template('edit.html', current_page='edit', task=task, group_name=group_name, groups=groups)

@main.route('/profile/delete/<task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.upcoming'))


@main.route('/profile/upcoming')
def upcoming():
    groups = Group.query.filter_by(user_id=current_user.id).all()

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    task_num = len(tasks)
    return render_template('upcoming.html', tasks=tasks, current_page='upcoming', groups=groups, task_num=task_num)

@main.route('/profile/task/<task_id>')
def task(task_id):
    groups = Group.query.filter_by(user_id=current_user.id).all()

    task = Task.query.get(task_id)
    group_name = Group.query.filter_by(id=task.group_id).first().group_name
    return render_template('task.html', current_page='task', task=task, group_name=group_name, groups=groups)

@main.route('/profile/group/<group_id>')
def group(group_id):
    groups = Group.query.filter_by(user_id=current_user.id).all()

    group = Group.query.get(group_id)
    group_name = Group.query.filter_by(id=group_id).first().group_name

    current_page = group.id
    tasks = Task.query.filter_by(group_id=group_id).all()
    task_num = len(tasks)
    return render_template('group.html', tasks=tasks, current_page=current_page, groups=groups, task_num=task_num, group_name=group_name)

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
def start():
    groups = Group.query.filter_by(user_id=current_user.id).all()

    return render_template('start.html', current_page='start', groups=groups)


@main.route('/profile/complete/<task_id>')
def complete(task_id):
    task = Task.query.get(task_id)
    if task.status == 'completed':
        task.status = 'pending'
    else:
        task.status = 'completed'
    db.session.commit()
    return redirect(url_for('main.profile'))
