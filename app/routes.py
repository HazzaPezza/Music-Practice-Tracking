from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, EditProfile, PracticeSessionForm
from werkzeug.security import generate_password_hash
from app import db
from app.models.track import User, PracticeSession

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
        print("Debug: User already authenticated") # DEBUG
        return redirect(url_for('main.profile'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(f"Debug: User found: {user}") # DEBUG
        
        if user and user.check_password(form.password.data):
            print("Debug: Password check passed") # DEBUG
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.profile'))
        else:
            print("Debug: Password check failed") # DEBUG
            flash('Login Unsuccessful...', 'danger')
            
    return render_template('login.html', form=form)


# ----- Profile and Logout Routes and API Endpoints -----
@main_bp.route('/profile')
@login_required
def profile():
    sessions = PracticeSession.query.filter_by(user_id=current_user.id).order_by(PracticeSession.date.desc()).limit(10).all()
    return render_template('profile.html', user=current_user, sessions=sessions)

@main_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    if form.validate_on_submit():
        current_user.userdetails.user_bio = form.user_bio.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('edit_profile.html', form=form)


@main_bp.route('/logout')
def logout():
    logout_user() # Clears the session
    return redirect(url_for('main.login'))


# ----- Practice Session and Note Routes and API Endpoints -----
from datetime import timedelta

@main_bp.route('/add_session', methods=['GET', 'POST'])
def add_session():
    form = PracticeSessionForm()
    if form.validate_on_submit():
        # Combine hours and minutes into a timedelta object
        session_duration = timedelta(hours=form.hours.data, minutes=form.minutes.data)
        
        new_session = PracticeSession(
            user_id=current_user.id, # Assuming you're using Flask-Login
            date=form.date.data,
            instrument=form.instrument.data,
            duration=session_duration,
            notes=form.notes.data
        )
        db.session.add(new_session)
        db.session.commit()
        return redirect(url_for('main.profile'))
        
    return render_template('add_session.html', form=form)


