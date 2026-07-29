import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "a8f3c1b9d2e7f4a6c0b5d8e1f2a3b4c5")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{DB_PATH}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://localhost:4000", "http://localhost:5173"])