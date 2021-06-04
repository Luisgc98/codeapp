from flask.helpers import url_for
from werkzeug.utils import redirect
from . import auth
from flask import render_template, request, flash
from .forms import LoginForm, RegisterStudentForm, RegisterTeacherForm
from flask_login import login_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        user = form.validateUser()
        if type(user) == str:
            flash(user)
            return redirect(url_for('auth.login'))
        else:
            login_user(user)
            flash('Bienvenido')
            return redirect(url_for('main.home'))
    
    return render_template('auth/login.html', form=form)

@auth.route('/register_student', methods=['GET', 'POST'])
def registerStudent():
    form = RegisterStudentForm()

    if request.method == 'POST':
        user_valid = form.validateIdentifier()
        if type(user_valid) == str:
            flash(user_valid)
            return redirect(url_for('auth.login'))
        elif user_valid == False:
            flash('Usuario ya existente.')
            return redirect(url_for('auth.register'))
        else:
            flash('Identificador no válido.')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/registerStudent.html', form=form)

@auth.route('/register_teacher', methods=['GET', 'POST'])
def registerTeacher():
    form = RegisterTeacherForm()

    if request.method == 'POST':
        print(form.license.data)
    
    return render_template('auth/registerTeacher.html', form=form)