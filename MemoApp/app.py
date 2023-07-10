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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    Administrator = db.Column(db.Boolean)

    @property
    def is_Administrator(self):
        return self.Administrator

#ボードの確認
class Boards(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    # available_user = db.Column(pg.ARRAY(db.Integer, dimensions=1))

#ボード
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writeuserid = db.Column(db.Integer)
    text = db.Column(db.Text())
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

#管理者画面
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_Administrator
admin = Admin(app, '管理者画面')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Boards, db.session))
admin.add_view(MyModelView(Board, db.session))

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
    # Boards = Boards.query.all()
    return render_template('index.html')

#ボード画面
@app.route('/board')
@login_required
def board():
    Boardinfo = Board.query.all()
    return render_template('board.html',Boardinfo=Boardinfo)

if __name__ == '__main__':
    app.run(debug=True)
