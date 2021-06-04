from flask import flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from models import User
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
                password=self.password,
                pwhash=user_db.password
                ):
                return user_db
            else:
                return 'Contraseñas no coinciden.'
        else:
            return 'Usuario no registrado.'

class RegisterForm(FlaskForm):
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
                user_id=User._getCountUser(),
                user_name=self.user_name,
                email=self.email,
                password=generate_password_hash(self.password)
            )
            return User.addUser(user)