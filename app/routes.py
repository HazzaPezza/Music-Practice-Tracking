from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import SignUpForm
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
@main_bp.route('/login', methods = ['GET', 'POST'])
def login():
  return render_template('login.html')
