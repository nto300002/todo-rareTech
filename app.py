import datetime
from datetime import timedelta
import secrets
from nis import match
from turtle import title
from unittest import result
from flask_mysqldb import MySQL, MySQLdb
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from passlib.hash import sha256_crypt
from forms import RegistrationForm, TaksForm
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

@app.route('/login', methods=["GET", "POST"])
@for_guests
def login():
    if request.method == "POST":
        #ユーザーデータをフォームから取得
        email = request.form['email']
        plain_pw = request.form['password']

        #カーソルを作成しDBに問い合わせる
        curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = curr.execute("SELECT * FROM users WHERE email=%s", (email,))

        #合致しているかチェック
        if result:
            #クエリの結果からユーザーデータを保存する
            user_data = curr.fetchone()
            hashed_pw = user_data['password']
        
            #パスワードのバリデーション
            if sha256_crypt.verify(plain_pw, hashed_pw):
                #セッションを保存する
                session['logged_in'] = True
                session['email'] = user_data['email']
                session['username'] = user_data['username']

                #todo一覧へリダイレクト
                flash("Login success.", "success")
                return redirect(url_for("user_todo"))
        
        return render_template('login.html', title="Login", err='ログインが無効です')

    return render_template('login.html', title="Login")

# Route for the logout page.
@app.route("/logout")
@login_required
def logout():
    # Clear the user session then redirect them to login page.
    session.clear()
    flash("You are now logged out.", "info")
    return redirect(url_for("login"))

#一覧ページ
@app.route('/user_todo', methods=['GET', 'POST'])
@login_required
def user_todo():
    curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute("SELECT * FROM tasks WHERE author=%s", (session['username'],))
    tasks = curr.fetchall()
    curr.close()

    return render_template('user_todo.html', title='おぼえがき一覧', tasks = tasks)

#詳細ページ
@app.route('/todo/<int:id>', methods=['GET', 'POST'])   
@login_required
def todo(id):
    curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute("SELECT * FROM tasks WHERE id=%s", (id, ))
    tasks = curr.fetchall()
    curr.close()

    return render_template('todo.html', title='おぼえがき', tasks=tasks[0])

#todo作成ページ
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TaksForm(request.form)
    if request.method == 'POST':
        #タスクを取得する
        title = form.title.data
        detail = form.detail.data
        created_at = datetime.datetime.today()
        author = session['username']

        #カーソルを作成しDBに問い合わせる
        curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curr.execute("INSERT INTO tasks(title, detail, created_at, author) VALUES(%s, %s, %s, %s)", (title, detail, created_at, author))

        #コミットしクローズする
        mysql.connection.commit()
        curr.close()

        #フラッシュを表示し、todo一覧へ
        flash('おぼえがきを追加', 'success')
        return redirect(url_for('user_todo'))

    return render_template('create.html', title='おぼえがきを追加', form=form)

#削除処理
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute("DELETE from tasks WHERE id =%s", (id, ))

    mysql.connection.commit()
    curr.close()

    flash("削除しました", "warning")
    redirect(url_for("user_todo"))

    return render_template('user_todo.html', title='おぼえがき一覧')

#編集処理
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = TaksForm(request.form)
    if request.method == "POST":
        title = form.title.data
        detail = form.detail.data
        update_at = datetime.datetime.today()

        curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curr.execute("UPDATE tasks SET title = %s, detail = %s, update_at = %s WHERE id = %s", (title, detail, update_at, id))
        mysql.connection.commit()
        curr.close()

        return redirect(url_for("user_todo"))
    
    curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute("SELECT * FROM tasks WHERE id=%s", (id, ))
    tasks = curr.fetchall()

    mysql.connection.commit()
    curr.close()

    return render_template('edit.html', title='編集', form=form, tasks=tasks[0])


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
