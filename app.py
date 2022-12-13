import datetime
from datetime import timedelta
import secrets
from nis import match
from turtle import title
from flask_mysqldb import MySQL
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from passlib.hash import sha256_crypt
from forms import RegistrationForm
from access_control import login_required, for_guests

app = Flask(__name__)

app.permanent_session_lifetime = timedelta(minutes=5)
secret = secrets.token_urlsafe(32)
#環境設定を読み込む 
app.config.from_object(__name__)
app.config.update(dict(
  MYSQL_HOST='localhost',
  MYSQL_USER='yasuda',
  MYSQL_PASSWORD='fjei34',
  MYSQL_DB='tododb',
  SECRET_KEY=secret
))

mysql = MySQL()
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', title="Top")

@app.route('/index_nologin')
def index_nologin():
    return render_template('index_nologin.html')

@app.route('/register', methods=['GET','POST'])
@for_guests
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        #ユーザーデータ取得
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        create_at = datetime.datetime.today()
        
        #データベースのクエリを生成
        curr = mysql.connection.cursor()

        #データベースを選択
        curr.execute('''USE tododb''')

        #ユーザーネームが登録されているか確認
        matches = curr.execute("SELECT * FROM users WHERE username = %s", (username,))
        if matches:
            return render_template("register.html", title="新規登録", form=form, err="ユーザーネームはすでに登録されています")
        
        #メールアドレスが登録されているか確認
        matches = curr.execute("SELECT * FROM users WHERE email = %s", (email,))
        if matches:
            return render_template("register.html", title="新規登録", form=form, err="メールアドレスはすでに登録されています")

        #データベースにユーザーデータを保存
        curr.execute("INSERT INTO users(username, email, password, create_at) VALUES(%s, %s, %s, %s)", (username, email, password, create_at))

        #データベースの接続を終了
        mysql.connection.commit()
        curr.close()

        #ユーザーをリダイレクトする
        flash("アカウントを作成しました", "success")
        return redirect(url_for("user_todo"))

        
    return render_template('register.html', title="新規作成", form=form)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user_todo')
def user_todo():
    return render_template('user_todo.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/user', methods=['GET', 'POST'])
def CONNECT_DB():
    if request.method == 'GET':
        CS = mysql.connection.cursor()
        CS.execute('''USE tododb''')
        CS.execute('''SELECT * FROM users''')
        results = CS.fetchall()
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
