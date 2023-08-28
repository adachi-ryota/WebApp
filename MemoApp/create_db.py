from app import app, db, User, Boards, Memo
from  werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    user = User(username='admin', password=generate_password_hash('admin', method='sha256'), Administrator=True)
    boards = Boards(title="home",browsing=0,createfor=0)
    memo = Memo(board_id=1, writeuserid=0, text="ようこそ", memocolor="color1", x=850, y=350)

    db.session.add(user)
    db.session.add(boards)
    db.session.add(memo)
    db.session.commit()