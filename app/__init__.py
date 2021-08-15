from flask import Flask, render_template, request, url_for, Response, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'super secret key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models