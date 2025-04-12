# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reviews(db.Model):
	__tablename__ = "reviews"
	id = db.Column(db.Integer, primary_key=True)
	label = db.Column(db.String(100), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	body = db.Column(db.String(1000))