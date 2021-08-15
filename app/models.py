from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), index=True, nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    subtitle = db.Column(db.String(255), index=True, nullable=False)
    photo = db.Column(db.BLOB)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, unique=True, nullable=False)
    likes = db.Column(db.Integer, index=True, nullable=False, default=0)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)


class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.BLOB,  nullable=False)
    components = db.Column(db.Text, index=True, nullable=False)
    description = db.Column(db.Text, index=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
