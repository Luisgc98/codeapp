from . import main
from flask import redirect, url_for, render_template, request, flash, current_app
from flask_login import current_user, login_required
from .forms import AddGroupForm, AddSubjectForm, EditSubjectForm
from models import ClassGroup, ClassSubject, ClassTheme, Task
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

@main.route('/generate_code/<table>', methods=['GET', 'POST'])
@login_required
def generateCode(table):
    if table == 'group':
        query = str(ClassGroup._getCountGroups())
        if(len(query) < 2): query = '0'+query
        result = 'GROUP_'+query
    elif table == 'subject':
        query = str(ClassSubject._getCountSubjects())
        if(len(query) < 2): query = '0'+query
        result = 'SUBJECT_'+query
    return result

@main.route('/group/<group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):
    form_subject = AddSubjectForm()
    form_edit_subject = EditSubjectForm()
    group = ClassGroup._getGroup(group_id=group_id)
    subjects = ClassSubject._getSubjectsGroup(group_id=group.group_id)
    activities = Task._getTasksGroup(group_id=group.group_id)
    
    return render_template('main/group.html', 
                           user=current_user, 
                           group=group, 
                           subjects=subjects,
                           activities=activities,
                           themes=None,
                           form_subject=form_subject,
                           form_edit_subject=form_edit_subject)

@main.route('/add_subject/<group_id>', methods=['GET', 'POST'])
@login_required
def addSubject(group_id):
    form = AddSubjectForm()
    
    if request.method == 'POST':
        subject_valid = form.addSubject()
        if type(subject_valid) == str:
            flash(subject_valid)
        else:
            flash('Materia ya existente.')
        return redirect(url_for('main.group', group_id=group_id))
    
@main.route('/delete_subject/<subject_id>', methods=['GET', 'POST'])
@login_required
def deleteSubject(subject_id):
    subject = ClassSubject._getSubject(subject_id)
    group_id = subject.group_id
    msg = ClassSubject.deleteSubject(subject)
    flash(msg)
    return redirect(url_for('main.group', group_id=group_id))

@main.route('/edit_subject', methods=['GET', 'POST'])
@login_required
def editSubject():
    form = EditSubjectForm()
    
    if request.method == 'POST':
        subject = ClassSubject._getSubject(form.subject_id.data)
        group_id = subject.group_id
        form.times.data = request.form['init_time'] + ' a: ' +request.form['end_time']
        form.times.data = form._setTimes(subject)
        msg = ClassSubject.editSubject(subject, form)
        flash(msg)
        return redirect(url_for('main.group', group_id=group_id))

@main.route('/themes_subject/<subject_id>', methods=['GET', 'POST'])
@login_required
def themes_subject(subject_id):
    themes = ClassTheme._getThemesSubject(subject_id=subject_id)
    
    return render_template('fragments/themes_subject.html', themes=themes)

@main.route('/upload_file/<group_id>', methods=['GET', 'POST'])
def upload(group_id):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if request.method == 'POST':
        file = request.files['theme_file']
        filename = file.filename
        dirs = os.listdir(upload_folder)
        path = os.path.join(upload_folder, str(group_id), filename)
        file.save(path)
        flash('Archivo subido con éxito.')
        
        return redirect(url_for('main.group', group_id=group_id))
    
@main.route('/get_values_subject/<subject_id>')
def getValuesSubject(subject_id):
    form = EditSubjectForm()
    subject = ClassSubject._getSubject(class_id=subject_id)
    context = (str(subject.class_id), str(subject.class_name), str(subject.class_code))
    #return render_template('modal/edit_subject_page.html', form_edit_subject=form, subject=context)
    return (
        str(subject.class_id)+'/-'
        +str(subject.class_code)+'/-'
        +str(subject.class_name)+'/-'
        +str(subject.times)
    )