from . import main
from flask import redirect, url_for, render_template
from flask_login import current_user

@main.route('/home', methods=['GET', 'POST'])
def home():

    return render_template('main/home.html', user=current_user)