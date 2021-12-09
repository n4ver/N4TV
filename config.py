import os

APP_FOLDER = os.path.dirname(__file__)
HOST = '127.0.0.1'
PORT = 5000

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

SQLALCHEMY_BINDS = {
    'users': 'mysql://root:password@localhost/accounts',
    'games': 'mysql://root:password@localhost/games'
}

try:
    with open('KEY.txt', 'r') as f:
        SECRET_KEY = f.read()
except FileNotFoundError:
    SECRET_KEY = ''