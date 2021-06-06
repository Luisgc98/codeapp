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
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(length=80))
    email = db.Column(db.String(length=200), unique=True)
    password = db.Column(db.String(length=100))

    @staticmethod
    def _byID(id):
        return User.query.filter_by(id=id).first()

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
            return 'Maestro registrado correctamente'
        except:
            db.session.rollback()
            return 'Hubo un error al ingresar el usuario, inténtelo mas tarde.'

class UserRole(db.Model):
    user_role_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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
    teacher_id = db.Column(db.String(length=100), db.ForeignKey('user.id'))

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
    def _getByTeacher(teacher_id):
        return ClassRoom.query.filter_by(teacher_id=teacher_id).first()

    @staticmethod
    def addClassRoom(room):
        try:
            db.session.add(room)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

class ClassGroup(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_code = db.Column(db.String(length=10), unique=True)
    class_subject = db.Column(db.String(length=30))
    times = db.Column(db.String(length=30), default="09:00am-06:00pm")
    room_id = db.Column(db.Integer, db.ForeignKey('class_room.room_id'))

    @staticmethod
    def _getCountGroups():
        count = ClassGroup.query.all()
        if count is None: 
            count = 1
        else:
            count = len(count)
        return count

    @staticmethod
    def _getGroupCode(code):
        return ClassGroup.query.filter_by(group_code=code).first()

    @staticmethod
    def _getGroup(group_id=None, all=False):
        if all:
            return ClassGroup.query.all()
        return ClassGroup.query.filter_by(group_id=group_id).first()

    def _getTeacherGroup(self):
        teacher = User.query.filter_by(
            id= ClassRoom.query.filter_by(
                room_id=self.room_id
            ).first().teacher_id
        ).first()
        return teacher

    def _getTasksGroup(self, count=False):
        tasks = Task.query.filter_by(group_id=self.group_id).first()
        if count and tasks:
            tasks = len(tasks)
        elif tasks is None and count:
            tasks = 'Ninguna'
        return tasks
    
    @staticmethod
    def addGroup(group):
        try:
            db.session.add(group)
            db.session.commit()
            return 'Grupo agregado con éxito.'
        except:
            db.session.rollback()
            return 'Hubo un error, intente de nuevo más tarde.'

class StudentClass(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('class_group.group_id'))

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

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('class_group.group_id'))
    task_description = db.Column(db.String(length=1000))
    deliverie_date = db.Column(db.Date)
    is_active = db.Column(db.String(length=1), default="Y")

    @staticmethod
    def _getCountTask():
        count = Task.query.all()
        if count is None: 
            count = 1
        else:
            count = len(count)
        return count

    @staticmethod
    def addTask(task):
        try:
            db.session.add(task)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False