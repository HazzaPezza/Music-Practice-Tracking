from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
  # Define the User model with id, username, email, and password_hash fields.
  # The id is the primary key, username and email are indexed and unique, and password_hash stores the hashed password.
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(255))

  def set_password(self, password):
    # Hash the password using scrypt and store it in the password_hash field.
    self.password_hash = generate_password_hash(password, method='scrypt')

  def check_password(self, password):
    # Check if the provided password matches the stored password hash.
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<User {}>'.format(self.username)
  