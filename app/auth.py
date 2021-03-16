from flask import Blueprint, render_template, request, url_for, flash
from flask_login import login_user, logout_user
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app.models import User, db

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user = User.query.filter_by(email=email).first()
        except OperationalError:
            new_user = User(email=email, username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        if user:
            flash('Email address already exists.')
            return redirect(url_for('auth.register'))

        new_user = User(email=email, username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('blog.index'))

    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog.index'))
