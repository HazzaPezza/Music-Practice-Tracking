from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm
from werkzeug.security import generate_password_hash
from app import db
from app.models.track import User, LoginForm

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
    form = SignUpForm() # 1. Instantiate the form

    # 2. This replaces all your manual 'if request.method == POST' and 'if len(password) < 8'
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data, method='scrypt')
        new_user = User(
            username=form.username.data.strip(), 
            email=form.email.data.strip().lower(), 
            password_hash=hashed_pw
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('main.sign_up'))
        except Exception as e:
            db.session.rollback()
            flash('An internal error occurred.', 'danger')
    else:
       print(f"Form errors: {form.errors}")

    # 3. GET Request or Failed Validation
    users = User.query.all()
    return render_template('sign-up.html', form=form, users=users)


# ----- Login Routes and API Endpoints -----
# Second gonna do login so that I know what I'm doing with that.
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if user exists and password matches
        if user and user.check_password(form.password.data):
            # This function creates the session for the user
            login_user(user, remember=form.remember_me.data)
            
            flash('Logged in successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('login.html', form=form)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main_bp.route('/logout')
def logout():
    logout_user() # Clears the session
    return redirect(url_for('login'))