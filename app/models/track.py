from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  # Define the User model with id, username, email, and password_hash fields.
  # The id is the primary key, username and email are indexed and unique, and password_hash stores the hashed password.
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(255))

  def __repr__(self):
    return '<User {}>'.format(self.username)
  