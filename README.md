# Notes API - Flask Auth Backend

## Project Description

This is a Flask backend for a notes app. It handles user signup, login,
logout and session based authentication, and lets each logged in user
create, read, update and delete their own notes. A user can never see or
change another user's notes. The index route for notes supports pagination
through `page` and `per_page` query params.

This project was built for the Full Auth Flask Backend summative lab. It
is meant to be paired with the sessions version of the provided client
repo.

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-RESTful
- Flask-Bcrypt
- Flask-CORS
- Marshmallow
- Faker
- SQLite

## Installation Instructions

1. Clone the repo and move into the project folder.
2. Install dependencies with pipenv:

   ```
   pipenv install
   pipenv shell
   ```

3. Move into the `server` folder, then set up the database:

   ```
   cd server
   export FLASK_APP=app.py
   flask db upgrade
   ```

4. Seed the database with starter data:

   ```
   python seed.py
   ```

## Run Instructions

From inside the `server` folder, with the pipenv shell active:

```
python app.py
```

The API will run on `http://localhost:5555`.

## Endpoints

### Auth

- `POST /signup` - creates a new user. Expects JSON body with `username`
  and `password`. Returns the new user and logs them in (starts a
  session) on success. Returns 422 if the username is taken or missing
  fields.
- `POST /login` - logs an existing user in. Expects JSON body with
  `username` and `password`. Returns 401 on bad credentials.
- `DELETE /logout` - logs the current user out by clearing the session.
  Returns 401 if no one is logged in.
- `GET /check_session` - returns the currently logged in user based on
  the session cookie. Returns 401 if nobody is logged in.

### Notes

All notes routes require an active session (the user must be logged in).

- `GET /notes` - returns a paginated list of the logged in user's notes.
  Accepts `page` and `per_page` query params (defaults are page 1, 10 per
  page). Response includes `notes`, `total`, `page`, `pages`, and
  `per_page`.
- `POST /notes` - creates a new note for the logged in user. Expects JSON
  body with `title` and `content`.
- `PATCH /notes/<id>` - updates a note's `title` and/or `content`. Only
  the note's owner can update it. Returns 403 if the note belongs to
  someone else, 404 if it does not exist.
- `DELETE /notes/<id>` - deletes a note. Only the note's owner can delete
  it. Returns 403 if the note belongs to someone else, 404 if it does not
  exist.

## Project Structure

```
server/
  app.py          flask app and all route resources
  config.py       app, db, bcrypt, migrate, api and cors setup
  models.py       User and Note models
  schemas.py      marshmallow schemas for serialization
  seed.py         seeds the database with fake users and notes
  migrations/     flask-migrate migration files
Pipfile
README.md
```
