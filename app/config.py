import os

dbdir = os.path.abspath(os.path.dirname(__file__))
updir = os.path.abspath(os.path.dirname(__file__))
from pathlib import Path
path = Path(dbdir)
dbdir = path.parent
path = Path(updir)
updir = path.parent
try:
    os.mkdir(os.path.join(updir, 'upload_folder'))
except:
    print('Carpeta de archivos ya creada')
    pass
class Config:
    SECRET_KEY = os.urandom(5)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dbdir, 'sinesis.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(updir, 'upload_folder/')