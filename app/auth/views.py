from flask.helpers import url_for
from werkzeug.utils import redirect
from . import auth
from flask import render_template, request, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        user = form.validateUser()
        if user:
            login_user(user)
            flash('Bienvenido')
            return redirect(url_for('main.home'))
        else:
            flash(user)
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        user_valid = form.registerUser()
        if user_valid:
            flash(user_valid)
            return redirect(url_for('auth.login'))
        else:
            flash('Usuario ya existente.')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', form=form)