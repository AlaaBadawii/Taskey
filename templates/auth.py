from sqlite3 import IntegrityError
from flask import Blueprint, request, redirect, render_template, flash, url_for
from flask_login import login_user, logout_user, login_required,current_user
from email_validator import validate_email, EmailNotValidError
from .models.user import User
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('This email does not exist.')
            return redirect(url_for('auth.login'))

        if not user.check_password(password):
            flash('Invalid email or password.')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            flash('Passwords do not match.')
            return redirect(url_for('auth.signup'))

        user_by_email = User.query.filter_by(email=email).first()
        user_by_username = User.query.filter_by(username=name).first()

        if user_by_email:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        if user_by_username:
            flash('Username already exists')
            return redirect(url_for('auth.signup'))

        VALID_EMAIL_DOMAINS = [
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com'
            # Add other known valid domains here
        ]

        # Validate email format
        try:
            valid = validate_email(email)
            email = valid.email  # Update with normalized form
        except EmailNotValidError as e:
            flash(str(e))
            return redirect(url_for('auth.signup'))

        # Validate email domain
        domain = email.split('@')[-1]
        if domain not in VALID_EMAIL_DOMAINS:
            flash('Invalid email domain.')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, username=name)
        new_user.set_password(password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.')
            return redirect(url_for('auth.signup'))

        return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    user_id = request.form.get('user_id')

    # Ensure the user exists and the user is authorized to delete the account
    user = User.query.get(user_id)
    if user:
        if current_user.id == user.id or current_user.is_admin:  # Assuming you have an is_admin attribute
            db.session.delete(user)
            db.session.commit()
            flash('User account deleted successfully.')
            return redirect(url_for('main.index'))
        else:
            flash('You are not authorized to delete this account.')
            return redirect(url_for('main.profile'))
    else:
        flash('User not found.')
        return redirect(url_for('main.profile'))
