from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_mysqldb import MySQL
from forms import ProductForm, LoginForm

bp_user_login = Blueprint('bp_user_login', __name__, url_prefix='/user_login')
mysql=MySQL() 
@bp_user_login.route('/', methods=['GET', 'POST'])
def user_login():
    print('user_login')
    form = LoginForm()
    if form.validate_on_submit():
        print('validated user_login')
        
        print(request.form['password'])
        if request.method =='POST':
            username = request.form['username']
            print(username)
            password = request.form['password']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()
            if account:
                print(account)
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                return redirect(url_for('bp_dashboard.dashboard'))
            else:
                flash('Incorrect username/password!', 'error')
                print('Incorrect username/password!', 'error')
    else:
        print('not validated user_login', form.errors)
        print("This is username", request.form['username'])
        print("This is username", request.form['password'])
    return render_template('user_login.html')