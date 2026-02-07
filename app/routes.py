from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
  """
  This is just a return function for the index route. Decorators above
  provide the URLs that this function is mapped to through app.route().

  :return: Returns render_template response which renders index.html
  """
  return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/sign-up')
def sign_up():
  return render_template('sign-up.html')
  