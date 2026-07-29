from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, Note
from schemas import user_schema, note_schema, notes_schema


class Signup(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "username and password are required"}, 422

        if User.query.filter_by(username=username).first():
            return {"error": "username already taken"}, 422

        try:
            user = User(username=username)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()
        except ValueError as error:
            db.session.rollback()
            return {"error": str(error)}, 422

        session["user_id"] = user.id
        return user_schema.dump(user), 201


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if not user_id:
            return {"error": "not authorized"}, 401

        user = User.query.filter(User.id == user_id).first()

        if not user:
            return {"error": "not authorized"}, 401

        return user_schema.dump(user), 200


class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            session["user_id"] = user.id
            return user_schema.dump(user), 200

        return {"error": "invalid username or password"}, 401


class Logout(Resource):
    def delete(self):
        if not session.get("user_id"):
            return {"error": "not authorized"}, 401

        session["user_id"] = None
        return {}, 204


class Notes(Resource):
    def get(self):
        user_id = session.get("user_id")

        if not user_id:
            return {"error": "not authorized"}, 401

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        pagination = Note.query.filter_by(user_id=user_id).order_by(
            Note.id.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        return {
            "notes": notes_schema.dump(pagination.items),
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page,
        }, 200

    def post(self):
        user_id = session.get("user_id")

        if not user_id:
            return {"error": "not authorized"}, 401

        data = request.get_json() or {}

        try:
            note = Note(
                title=data.get("title"),
                content=data.get("content"),
                user_id=user_id,
            )
            db.session.add(note)
            db.session.commit()
        except ValueError as error:
            db.session.rollback()
            return {"error": str(error)}, 422

        return note_schema.dump(note), 201


api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Notes, "/notes")


if __name__ == "__main__":
    app.run(port=5555, debug=True)