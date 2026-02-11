from flask import render_template
from app import app

# ----- Index Routes and API Endpoints -----
@app.route('/')
@app.route('/index')
def index():
  """
  This is just a return function for the index route. Decorators above
  provide the URLs that this function is mapped to through app.route().

  :return: Returns render_template response which renders index.html
  """
  return render_template('index.html')


# Going to start with sign up and post operations to DB.
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
  return render_template('sign-up.html')



# ----- Sign-up Routes and API Endpoints -----
# Going to start with sign up and post operations to DB.
@app.route('/sign-up')
def sign_up():
  return render_template('sign-up.html')


# ----- Login Routes and API Endpoints -----
# Second gonna do login so that I know what I'm doing with that.
@app.route('/login')
def login():
  return render_template('login.html')
