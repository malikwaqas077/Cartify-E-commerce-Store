from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
import mysql.connector
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'flasapp-server.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'vhuqfqlnqk'
app.config['MYSQL_PASSWORD'] = 'Malik786'
app.config['MYSQL_DB'] = 'flaskauthapp-database'
mysql = MySQL(app)

# User registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up')

# User login form
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Sign In')

# Routes
@app.route('/')
def home():
    return 'Welcome to the Flask Azure App!'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (form.username.data, form.password.data))
        mysql.connection.commit()
        cursor.close()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (form.username.data, form.password.data))
        user = cursor.fetchone()
        cursor.close()
        if user:
            flash('Login successful!', 'success')
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

