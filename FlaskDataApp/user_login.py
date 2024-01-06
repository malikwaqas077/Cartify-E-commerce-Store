from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_mysqldb import MySQL
from forms import ProductForm, LoginForm

bp_user_login = Blueprint('bp_user_login', __name__, url_prefix='/user_login')
mysql=MySQL() 
@bp_user_login.route('/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[2]
            session['username'] = account[1]
            return redirect(url_for('view_dashboard'))  # Update this to your dashboard route
        else:
            flash('Incorrect username/password!', 'error')
    else:
        if form.is_submitted():
            print('Form errors:', form.errors)  # Will print form validation errors if any

    return render_template('user_login.html', form=form)
