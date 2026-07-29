from random import choice

from faker import Faker

from config import app, db
from models import User, Note

fake = Faker()

with app.app_context():
    print("clearing tables...")
    Note.query.delete()
    User.query.delete()

    print("seeding users...")
    users = []
    usernames = set()
    while len(usernames) < 5:
        usernames.add(fake.user_name())

    for username in usernames:
        user = User(username=username)
        user.password_hash = "password123"
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("seeding notes...")
    notes = []
    for _ in range(30):
        note = Note(
            title=fake.sentence(nb_words=4),
            content=fake.paragraph(nb_sentences=3),
            user_id=choice(users).id,
        )
        notes.append(note)

    db.session.add_all(notes)
    db.session.commit()

    print(f"seeded {len(users)} users and {len(notes)} notes")