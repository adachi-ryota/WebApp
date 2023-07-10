from app import app, db, User
from  werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    user = User(username='admin', password=generate_password_hash('admin', method='sha256'), Administrator=True)
    db.session.add(user)
    db.session.commit()