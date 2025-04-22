from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Explicitly point Flask to the correct templates folder
template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

app = Flask(__name__, template_folder=template_path)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from app.views import routes
