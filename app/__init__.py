from flask import Flask

# Instantiate flask app from environment variable.
app = Flask(__name__)

# Import routes, imported here to avoid circular imports.
from app import routes
