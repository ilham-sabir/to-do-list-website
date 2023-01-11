#app.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 
import psycopg2.extras
import urllib.request
import re 
import os
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:helloIlham123@localhost:5432/ilhame'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def loginin():
  return render_template('login.html')

@app.route("/about")
def aboutus():
  return render_template("aboutus.html")

@app.route("/todo")
def doit():
  return render_template("todo.html")

app.secret_key = 'ilhameIlham1996'
 
DB_HOST = "localhost"
DB_NAME = "ilhame"
DB_USER = "postgres"
DB_PASS = "helloIlham123"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

#...................................................................................................................................
# this part is for login file
@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['email'] = account['email']
                # Redirect to home page
                return redirect(url_for('doit'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')
#.................................................................................................................
# this part is for register file
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'firstname' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password= request.form['password']
    
        _hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', firstname):
            flash('Firstname must contain only characters and numbers!')
        elif not re.match(r'[A-Za-z0-9]+', lastname):
            flash('Lastname must contain only characters and numbers!')
        elif not firstname or not lastname or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO users (firstname, lastname, email, password) VALUES (%s,%s,%s,%s)", (firstname, lastname, email, _hashed_password))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
       # Form is empty... (no POST data)
       flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

#..........................................................
#this code is for todo list file
class user(db.Model):
    __tablename__='todo'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    complete=db.Column(db.Boolean)

def __init__(self,title, complete):
    self.title=title
    self.complete=complete

@app.route('/todoit')
def dolist():
    # show all todos
    todo_list = user.query.all()
    return render_template('todo.html', todo_list=todo_list)
@app.route("/add", methods=["POST"])
def add():
    # add new todo
    title=request.form.get("title")
    new_todo = user(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("dolist"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    
    todo = user.query.filter_by(id=todo_id).first()
    todo.complete= not todo.complete
    db.session.commit()
    return redirect(url_for("dolist"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    
    todo = user.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("dolist"))

if __name__=='__main__':
       app.run(debug=True)