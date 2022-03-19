from flask import Flask, redirect, url_for, render_template, request
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="Yahvi$123", database="busApp")
cur = mydb.cursor()

app = Flask(__name__)

session = {'loggedin': False, 'email': ''}

@app.route('/', methods=["POST", "GET"])

def index():
    return render_template('index.html')

@app.route('/login', methods=["POST", "GET"])

def login():
    msg = ''
    if 'Email' in request.form and 'Password' in request.form:
        email = request.form["Email"]
        password = request.form["Password"]
        cur.execute('SELECT * FROM login WHERE email = %s AND password = %s', (email, password))
        account = cur.fetchone()
        print(account)
        # for account in accounts:
        if account:
            session['loggedin'] = True
            session['email'] = account[0]
            print(session['email'])
            return redirect(url_for('buses'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg = msg)
            
@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template('register.html')

@app.route('/registerResult', methods=["GET","POST"])
def registerResult():
    email = request.form["email"]
    password = request.form["pass"]
    name = request.form["name"]
    cur.execute('SELECT * FROM login WHERE email = %s', (email,))
    account = cur.fetchone()
    if account:
        return "Account Already Exists"
    else:
        cur.execute("INSERT INTO LOGIN VALUES('{}', '{}', '{}')".format(email, password, name))
        mydb.commit()
        return "Registered Successfully"

@app.route('/buses', methods=["GET","POST"])
def buses():
    cur.execute("SELECT * FROM buses")
    buses = cur.fetchall()
    print(buses)
    return render_template('buses.html', value = buses, lenght=len(buses))

@app.route('/ticket', methods=["GET","POST"])
def ticket():
    return render_template('ticket.html')

@app.route('/logout')
def logout():
   session['loggedin'] = False
   session['email'] = ''
   # Redirect to login page
   return redirect(url_for('login'))
# @app.route('')

if __name__ == "__main__":
    app.run(debug=True)
