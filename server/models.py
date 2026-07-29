from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("password_hash is not a readable attribute")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    @validates("username")
    def validate_username(self, key, username):
        if not username or not username.strip():
            raise ValueError("username must be present")
        return username

    def __repr__(self):
        return f"<User {self.id} {self.username}>"

class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @validates("title")
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("title must be present")
        return title

    @validates("content")
    def validate_content(self, key, content):
        if not content or not content.strip():
            raise ValueError("content must be present")
        return content

    def __repr__(self):
        return f"<Note {self.id} {self.title}>"