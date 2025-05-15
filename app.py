from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'employee_info'

mysql = MySQL(app)
 

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/check-user',methods=['POST'])
def check_user():
    try:
        data = request.get_json()

        username = data.get['username']
        password = data.get['password']

        salted = str(SALT + password).encode('utf-8')
        hash = hashlib.sha512(salted).hexdigest()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND passwords=%s", (username, hash))
        user = cur.fetchone()
        cur.close()

        if user:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
        
@app.route('/add_employees',methods=['POST'])
def add_employees():
    try:
        lname = request.form['lname']
        fname = request.form['fname']
        mname = request.form['mname']
        position = request.form['position']
        office = request.form['office']


        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE lname=%s, fname=%s, mname=%s, position=%s, office=%s", (lname, fname, mname, position, office))
        user = cur.fetchone()
        cur.close()

        if user:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
        






@app.route('/get-employees', methods=['GET'])
def get_employees():
   try:
       cur = mysql.connection.cursor()
       cur.execute("SELECT * FROM employee_information")
       employees = cur.fetchall()
       cur.close()

       return jsonify(employees)
   except Exception as e:
       return jsonify({"error": str(e)}), 500 


if __name__ == '__main__':
    app.run(debug=True)








