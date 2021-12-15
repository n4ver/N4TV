from os import path

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    try:
        with open('KEY.txt', 'r') as f:
            SECRET_KEY = f.read()
    except FileNotFoundError:
        SECRET_KEY = ''

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/app.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        'users': 'sqlite:///../db/users.db',
        'games': 'sqlite:///../db/games.db'
    }

    
'''
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.sqlite3'

    SQLALCHEMY_BINDS = {
        'users': 'mysql://root:password@localhost/accounts',
        'games': 'mysql://root:password@localhost/games'
    }

    try:
        with open('KEY.txt', 'r') as f:
            SECRET_KEY = f.read()
    except FileNotFoundError:
        SECRET_KEY = ''
'''