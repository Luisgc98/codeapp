from . import main
from flask import redirect, url_for, render_template, request, flash
from flask_login import current_user, login_required
from .forms import AddGroupForm
from models import ClassGroup

@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    groups = ClassGroup._getGroup(all=True)
    print(groups)

    return render_template('main/home.html', user=current_user, groups=groups)

@main.route('/add_group/<send>', methods=['GET', 'POST'])
@main.route('/add_group', methods=['GET', 'POST'])
@login_required
def addGroup(send=False):
    form = AddGroupForm()
    
    if send and request.method == 'POST':
        print(current_user)
        group_valid = form.addGroup(current_user)
        if type(group_valid) == str:
            flash(group_valid)
        else:
            flash('Grupo ya existente.')
        return redirect(url_for('main.home'))
    
    return render_template('modal/add_group_page.html', form=form)

@main.route('/generate_code', methods=['GET'])
@login_required
def generateCode():
    query = str(ClassGroup._getCountGroups())
    if(len(query) < 2): query = '0'+query
    result = 'GROUP_'+query

    return result