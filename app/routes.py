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
  if request.method == 'POST':
    print(f"ALL FORM DATA: {request.form}")

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    print("Username: {}, Email: {}, Password: {}".format(username, email, password))

    if username and email and password:
      hashed_pw = generate_password_hash(password, method='scrypt')

      new_user = User(username=username, email=email, password_hash=hashed_pw)
      db.session.add(new_user)
      db.session.commit()
      
      return redirect(url_for('main.sign_up'))
  
  users = User.query.all()
  return render_template('sign-up.html', users=users)


# ----- Login Routes and API Endpoints -----
# Second gonna do login so that I know what I'm doing with that.
@main_bp.route('/login')
def login():
  return render_template('login.html')
