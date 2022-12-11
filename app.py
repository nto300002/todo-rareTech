from flask_mysqldb import MySQL
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

mysql = MySQL()
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index_nologin')
def index_nologin():
    return render_template('index_nologin.html')

@app.route('/register', methods=['GET','POST'])
def register():
    # if request.method == 'POST':
    #     name = request.form['name']
    #     email = request.form['email']
    #     password = request.form['password']
    #     cursor = mysql.connection.cursor()
    #     cursor.execute('''USE tododb''')
    #     cursor.execute(''' INSERT INTO users VALUES(%s,%s,%s, NULL, NULL) ''',(name, email, password))
    #     mysql.connection.commit()
    #     cursor.close()
    #     return f"ユーザーを登録しました"
    return render_template('register.html')

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
