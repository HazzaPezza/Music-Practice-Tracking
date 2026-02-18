from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from app import db
from app.models.track import User
main_bp = Blueprint('main', __name__)

# ----- Index Routes and API Endpoints -----
@main_bp.route('/')
@main_bp.route('/index')
def index():
  """
  This is just a return function for the index route. Decorators above
  provide the URLs that this function is mapped to through app.route().

  :return: Returns render_template response which renders index.html
  """
  return render_template('index.html')


# ----- Sign-up Routes and API Endpoints -----
# Going to start with sign up and post operations to DB.
@main_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

  # If the method is POST (Form submitted) collect form information.
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # If none of the fields are empty generate a hashed password.
    if username and email and password:
      hashed_pw = generate_password_hash(password, method='scrypt')

      # After hashing password add the user to the database and commit the session.
      new_user = User(username=username, email=email, password_hash=hashed_pw)
      db.session.add(new_user)
      db.session.commit()
      
      # After adding the user redirect them back to sign up.
      return redirect(url_for('main.sign_up'))
  
  # This query takes all the user data in the db and passes it to template for display.
  users = User.query.all()
  return render_template('sign-up.html', users=users)


# ----- Login Routes and API Endpoints -----
# Second gonna do login so that I know what I'm doing with that.
@main_bp.route('/login')
def login():
  return render_template('login.html')
