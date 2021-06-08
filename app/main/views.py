from . import main
from flask import redirect, url_for, render_template, request, flash, current_app
from flask_login import current_user, login_required
from .forms import AddGroupForm
from models import ClassGroup, ClassSubject, Task
import os

@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = AddGroupForm()
    groups = ClassGroup._getGroup(all=True)

    return render_template('main/home.html', user=current_user, groups=groups, form=form)

@main.route('/add_group', methods=['GET', 'POST'])
@login_required
def addGroup():
    form = AddGroupForm()
    
    if request.method == 'POST':
        group_valid = form.addGroup(current_user)
        if type(group_valid) == str:
            flash(group_valid)
        else:
            flash('Grupo ya existente.')
        return redirect(url_for('main.home'))

@main.route('/delete_group/<group_id>', methods=['GET', 'POST'])
@login_required
def deleteGroup(group_id):
    group = ClassGroup._getGroup(group_id)
    msg = ClassGroup.deleteGroup(group)
    flash(msg)
    return redirect(url_for('main.home'))

@main.route('/generate_code', methods=['GET', 'POST'])
@login_required
def generateCode():
    query = str(ClassGroup._getCountGroups())
    if(len(query) < 2): query = '0'+query
    result = 'GROUP_'+query

    return result

@main.route('/group/<group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):
    group = ClassGroup._getGroup(group_id=group_id)
    subjects = ClassSubject._getSubjectsGroup(group_id=group.group_id)
    activities = Task._getTasksGroup(group_id=group.group_id)
    
    return render_template('main/group.html', 
                           user=current_user, 
                           group=group, 
                           subjects=subjects,
                           activities=activities)

@main.route('/upload_file/<group_id>', methods=['GET', 'POST'])
def upload(group_id):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if request.method == 'POST':
        file = request.files['theme_file']
        filename = file.filename
        dirs = os.listdir(upload_folder)
        if str(group_id) in dirs:
            pass
        else:
            os.mkdir(upload_folder+str(group_id))
        path = os.path.join(upload_folder, str(group_id), filename)
        file.save(path)
        flash('Archivo subido con éxito.')
        
        return redirect(url_for('main.group', group_id=group_id))