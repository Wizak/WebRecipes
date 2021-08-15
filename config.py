import os
import datetime


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    #     user='postgres',
    #     pw='admin',
    #     url='localhost:5431',
    #     db='recipes_base'
    # )
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)