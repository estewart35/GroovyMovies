# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from core.extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class Reviews(db.Model):
	__tablename__ = "reviews"
	id = db.Column(db.Integer, primary_key=True)
	label = db.Column(db.String(100), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	body = db.Column(db.String(1000))

	movie_id = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	user = db.relationship("Users", back_populates="reviews")


class Users(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(150), nullable=False)
	email = db.Column(db.String(150), unique=True, nullable=False)
	password = db.Column(db.String(150), nullable=False)

	reviews = db.relationship(
       "Reviews", back_populates="user", cascade="all, delete-orphan"
   	)

	def set_password(self, password):
		self.password = generate_password_hash(
      		password, method="pbkdf2:sha256", salt_length=16
		)

	def check_password(self, password):
		return check_password_hash(self.password, password)
	

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))