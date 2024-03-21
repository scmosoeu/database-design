import os
from dotenv import load_dotenv

from flask import Flask
from .extensions import db


def create_app():

    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    # Avoid getting warning messages
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app
