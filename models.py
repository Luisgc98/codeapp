from enum import unique
from app import db
from flask_login import UserMixin

'''class BaseMixin(db.Model):
    CREATE_BY = db.Column(db.Integer)
    CREATION_DATE = db.Column(db.Date)
    UPDATED_BY = db.Column(db.Integer)
    UPDATED_DATE = db.Column(db.Date)'''

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(length=80))
    email = db.Column(db.String(length=200), unique=True)
    password = db.Column(db.String(length=100))

    @staticmethod
    def _byID(id):
        return User.query.filter_by(user_id=id).first()

    @staticmethod
    def _byEmail(user_email):
        return User.query.filter_by(email=user_email).first()

    @staticmethod
    def _getCountUser():
        count = User.query.all()
        if count is None: 
            count = 1
        else:
            count = len(count)
        return count

    @staticmethod
    def addUser(user):
        try:
            db.session.add(user)
            db.session.commit()
            return 'Usuario agregado correctamente.'
        except:
            db.session.rollback()
            return 'Hubo un error al ingresar el usuario, inténtelo mas tarde.'