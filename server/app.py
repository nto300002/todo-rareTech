from flask_mysqldb import MySQL
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

app.config['MYSQL_PORT'] = 3306

mysql = MySQL()
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


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
