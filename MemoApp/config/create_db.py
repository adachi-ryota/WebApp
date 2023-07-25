from app import app, db, User, Boards
from  werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    user = User(username='admin', password=generate_password_hash('admin', method='sha256'), Administrator=True)
    boards = Boards(title="home")

    db.session.add(user)
    db.session.add(boards)
    db.session.commit()