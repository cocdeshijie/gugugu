from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm

@auth.before_app_request
def before_request():
    pass

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data.lower(),
                    password=form.password.data)
        form.check_username()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


