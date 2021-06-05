from flask import flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired
from models import Group, StudentClass, Teacher, User, ClassRoom, UserRole
from werkzeug.security import generate_password_hash, check_password_hash

validators = [DataRequired()]
class LoginForm(FlaskForm):
    user_name = StringField('', validators=validators)
    password = PasswordField('', validators=validators)
    submit = SubmitField('Conectar')

    def validateUser(self):
        user_db = User._byEmail(self.user_name.data)
        if user_db:
            if check_password_hash(
                password=self.password.data,
                pwhash=user_db.password
                ):
                return user_db
            else:
                return 'Contraseñas no coinciden.'
        else:
            return 'Usuario no registrado.'

class RegisterStudentForm(FlaskForm):
    user_name = StringField('', validators=validators)
    email = StringField('', validators=validators)
    password = PasswordField('', validators=validators)
    confirm_password = PasswordField('', validators=validators)
    identifier = StringField('', validators=validators)
    submit = SubmitField('Registrar')

    def registerUser(self):
        user_db = User._byEmail(self.email.data)
        if user_db:
            return False
        else:
            user = User(
                id=User._getCountUser(),
                user_name=self.user_name.data,
                email=self.email.data,
                password=generate_password_hash(self.password.data)
            )
            msg = User.addUser(user)
            role = UserRole(
                user_role_id = UserRole._getCountUsers(),
                user_id = user.id,
                role_id = 2
            )
            UserRole.addUserRole(role)
            user_class = StudentClass(
                class_id = StudentClass._getCountStudents(),
                room_id = ClassRoom.query.filter_by(room_code = self.identifier.data).first().id,
                student_id = user.id
            )
            StudentClass.addStudent(user_class)
            return msg

    def validateIdentifier(self):
        if Group._getGroupCode(self.identifier.data):
            self.registerUser()
        else:
            return None

specialtys = [
    ('', '--Especialidad--'),
    (1, 'Programación'),
    (2, 'Realidad Aumentada'),
    (3, 'Electricidad'),
    (4, 'Inteligencia artificial')
]
class RegisterTeacherForm(FlaskForm):
    user_name = StringField('', validators=validators)
    email = StringField('', validators=validators)
    specialty = StringField('', validators=validators)
    license = StringField('', validators=validators)
    password = PasswordField('', validators=validators)
    confirm_password = PasswordField('', validators=validators)
    submit = SubmitField('Registrar')

    def registerUser(self):
        user_db = User._byEmail(self.email.data)
        if user_db:
            return False
        else:
            user = Teacher(
                id=User._getCountUser(),
                user_name=self.user_name.data,
                email=self.email.data,
                password=generate_password_hash(self.password.data),
                user_license=self.license.data,
                specialty=self.specialty.data
            )
            msg = Teacher.addTeacher(user)
            role = UserRole(
                user_role_id = UserRole._getCountUsers(),
                user_id = user.id,
                role_id = 1
            )
            UserRole.addUserRole(role)
            class_room = ClassRoom(
                room_id= ClassRoom._getCountRooms(),
                teacher_id = user.id
            )
            class_room.generateCode()
            ClassRoom.addClassRoom(class_room)
            return msg