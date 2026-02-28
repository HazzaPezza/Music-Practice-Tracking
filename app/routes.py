from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import db
from app.models.track import User
import regex
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
        # 1. Extract and Clean Data
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password')

        # 2. Validations (Guard Clauses)
        # Username Length Check
        if not (5 <= len(username) <= 20):
            flash('Username must be between 5 and 20 characters.', 'danger')
            return redirect(url_for('main.sign_up'))

        # Check if Username or email already exists in db
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('main.sign_up'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('main.sign_up'))
        
        # Check password length.
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('main.sign_up'))
        
        # Check password has at least one uppercase letter and one digit.
        pattern = r"^(?=.*[A-Z])(?=.*\d).+$"
        if not regex.match(pattern, password):
            flash('Password must contain at least one uppercase letter and one digit.', 'danger')
            return redirect(url_for('main.sign_up'))

        # 3. Database Operation
        if username and email and password:
            hashed_pw = generate_password_hash(password, method='scrypt')
            new_user = User(username=username, email=email, password_hash=hashed_pw)
            
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('User created successfully!', 'success')
                return redirect(url_for('main.sign_up'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating user: {e}', 'danger')
                return redirect(url_for('main.sign_up'))

    # 4. GET Request: Display User List
    users = User.query.all()
    return render_template('sign-up.html', users=users)


# ----- Login Routes and API Endpoints -----
# Second gonna do login so that I know what I'm doing with that.
@main_bp.route('/login')
def login():
  return render_template('login.html')
