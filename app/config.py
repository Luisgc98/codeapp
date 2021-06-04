import os
dbdir = os.path.abspath(os.path.dirname(__file__))
from pathlib import Path
path = Path(dbdir)
dbdir = path.parent
class Config:
    SECRET_KEY = os.urandom(5)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dbdir, 'sinesis.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False