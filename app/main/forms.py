from flask import flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired
from models import ClassGroup, StudentClass, Teacher, User, ClassRoom, UserRole
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