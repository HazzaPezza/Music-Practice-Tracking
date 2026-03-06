from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

  db.init_app(app)
  migrate.init_app(app, db)

  with app.app_context():
    from .routes import main_bp
    app.register_blueprint(main_bp)

  return app

# Instantiate flask app from environment variable.
app = create_app()

with app.app_context():
  print(app.url_map)