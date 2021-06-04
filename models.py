from enum import unique
from app import db
from flask_login import UserMixin
from random import choice

'''class BaseMixin(db.Model):
    CREATE_BY = db.Column(db.Integer)
    CREATION_DATE = db.Column(db.Date)
    UPDATED_BY = db.Column(db.Integer)
    UPDATED_DATE = db.Column(db.Date)'''

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(length=20))

    @staticmethod
    def _getCountRole():
        count = Role.query.all()
        if count is None: 
            count = 1
        else:
            count = len(count)
        return count

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

class Teacher(User):
    user_license = db.Column(db.Integer, unique=True)
    specialty = db.Column(db.String)

    @staticmethod
    def addTeacher(user):
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

class UserRole(db.Model):
    user_role_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    @staticmethod
    def _getCountUsers():
        count = UserRole.query.all()
        if count is None: 
            count = 1
        else:
            count = len(count)
        return count

    @staticmethod
    def addUserRole(role):
        try:
            db.session.add(role)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

class ClassRoom(db.Model):
    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(length=30), default='Desconocido')
    room_code = db.Column(db.String(length=30), unique=True)
    teacher_id = db.Column(db.String(length=100), db.ForeignKey('user.user_id'))

    def generateCode(self):
        abc = 'abcdefghijklmnopqrstuvwxyz123456789'
        code = ''
        while len(code) < 10: code += choice(abc)
        self.room_code = code

    @staticmethod
    def _getCountRooms():
        count = ClassRoom.query.all()
        if count is None: 
            count = 1
        else:
            count = len(count)
        return count

    @staticmethod
    def _getRoomCode(code):
        return ClassRoom.query.filter_by(room_code=code).first()

    @staticmethod
    def addClassRoom(room):
        try:
            db.session.add(room)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

class StudentClass(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('class_room.room_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    @staticmethod
    def _getCountStudents():
        count = StudentClass.query.all()
        if count is None: 
            count = 1
        else:
            count = len(count)
        return count

    @staticmethod
    def addStudent(user):
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False