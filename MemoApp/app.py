from flask import Flask, render_template, request, redirect, current_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
#管理者画面
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os
from sqlalchemy.dialects import postgresql as pg
from  werkzeug.security import generate_password_hash, check_password_hash
# import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memo.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#ユーザ情報
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    Administrator = db.Column(db.Boolean)

    @property
    def is_Administrator(self):
        return self.Administrator

#ボード情報
class Boards(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    browsing = db.Column(db.Integer)
    createfor = db.Column(db.String)

#メモ情報
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer)
    writeuserid = db.Column(db.Integer)
    text = db.Column(db.Text())
    memocolor = db.Column(db.String(6))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

#管理者画面
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_Administrator
admin = Admin(app, '管理者画面')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Boards, db.session))
admin.add_view(MyModelView(Memo, db.session))

#ログイン画面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if username and password:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
            else:
                return render_template('login.html', message='Invalid username or password')
        else:
            return render_template('login.html', message='Not filled in username or password')
    else:
        return render_template('login.html')

#アカウント作成画面
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            user = User(username=username, password=generate_password_hash(password, method='sha256'), Administrator=False)

            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        else:
            return render_template('signup.html', message='Not filled in username or password')
    else:
        return render_template('signup.html')

#ログアウト
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

#基本画面
@app.route('/')
@login_required
def index():
    user=current_user
    boards1 = Boards.query.filter_by(browsing=user.id)
    boards2 = Boards.query.filter_by(browsing=0)
    return render_template('index.html',Boards1=boards1, Boards2=boards2)

#ボード作成画面
@app.route('/createboard', methods=['GET', 'POST'])
@login_required
def createboard():
    if request.method == 'POST':
        title = request.form.get('title')
        browsing = request.form.get('browsing')

        if title and browsing:
            board = Boards(title=title, browsing=browsing, createfor=current_user.id)

            db.session.add(board)
            db.session.commit()
            return redirect('/')
        else:
            return render_template('createboard.html', user=current_user, message='Not filled in title')
    else:
        return render_template('createboard.html', user=current_user)

# ボード削除画面
@app.route('/deleteboard', methods=['GET', 'POST'])
@login_required
def deleteboard():
    if request.method == 'POST':
        b_id = request.form.get('b_id')

        board = Boards.query.filter_by(board_id=b_id).first()
        db.session.delete(board)

        Memo.query.filter_by(board_id=b_id).delete()
    
        db.session.commit()

        return redirect("/")
    else:
        user = current_user
        boards = Boards.query.filter_by(createfor=user.id)
        return render_template('deleteboard.html', Boards=boards)

#ボード画面
@app.route('/board/<id>', methods=['GET', 'POST'])
@login_required
def board(id):
    if request.method == 'POST':
        text = request.form.get('newmemo')
        x = int(request.form.get('x'))
        y = int(request.form.get('y')) + 20
        memocolor = request.form.get('color')

        if memocolor and x and y:
            user=current_user
            memo = Memo(board_id=id, writeuserid=user.id, text=text,
                memocolor=memocolor, x=x, y=y)

            db.session.add(memo)
            db.session.commit()

    Boardinfo = Memo.query.filter_by(board_id=id)
    return render_template('board.html',Boardinfo=Boardinfo)

if __name__ == '__main__':
    app.run(debug=True)
