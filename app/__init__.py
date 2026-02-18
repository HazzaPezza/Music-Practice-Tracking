from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)

  with app.app_context():
    from .routes import main_bp
    app.register_blueprint(main_bp)

    from app.models.track import User
    db.create_all()

  return app

# Instantiate flask app from environment variable.
app = create_app()

  