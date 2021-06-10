import json
from flask import flash
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired
from models import ClassGroup, ClassSubject, StudentClass, Teacher, User, ClassRoom, UserRole
from werkzeug.security import generate_password_hash, check_password_hash

validators = [DataRequired()]
class AddGroupForm(FlaskForm):
    group_code = StringField('', validators=validators)
    room_id = HiddenField('', validators=validators)
    submit = SubmitField('Agregar')
    
    def _getRoomId(self, teacher_id):
        self.room_id.data = ClassRoom._getByTeacher(teacher_id).room_id
        return self.room_id.data
        
    def addGroup(self, user):
        group_db = ClassGroup._getGroupCode(self.group_code.data)
        if group_db:
            return False
        else:
            group = ClassGroup(
                group_id=ClassGroup._getCountGroups(),
                group_code = self.group_code.data,
                room_id=self._getRoomId(user.id)
            )
            msg = ClassGroup.addGroup(group)
            return msg

class AddSubjectForm(FlaskForm):
    subject_name = StringField('', validators=validators)
    class_code = StringField('', validators=validators)
    group_id = HiddenField('', validators=validators)
    submit = SubmitField('Agregar')
        
    def addSubject(self):
        subject_db = ClassSubject._getClassCode(self.class_code.data, self.group_id.data)
        if subject_db:
            return False
        else:
            subject = ClassSubject(
                class_id=ClassSubject._getCountSubjects(),
                class_name=self.subject_name.data,
                class_code=self.class_code.data,
                group_id=self.group_id.data,
                times = 'Sin especificar'
            )
            msg = ClassSubject.addSubject(subject)
            return msg
        
class EditSubjectForm(FlaskForm):
    new_name = StringField('Nombre de la materia', validators=validators)
    current_code = StringField('', validators=validators)
    subject_id = HiddenField('', validators=validators)
    times = StringField('', validators=validators)
    edit = SubmitField('Actualizar')
        
    def _setTimes(self, subject):
        times = subject._getTimesSubject()
        new_time = {str(len(times)):str(self.times.data)}
        times.update(new_time)
        return times
        
    def addSubject(self):
        subject_db = ClassSubject._getClassCode(self.class_code.data, self.group_id.data)
        if subject_db:
            return False
        else:
            subject = ClassSubject(
                class_id=ClassSubject._getCountSubjects(),
                class_name=self.subject_name.data,
                class_code=self.class_code.data,
                group_id=self.group_id.data,
                times = 'Sin especificar'
            )
            msg = ClassSubject.addSubject(subject)
            return msg