from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
import mysql.connector
from flask_mysqldb import MySQL
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import ValidationError
from flask import Flask
from models import db
from forms import ProductForm
from dashboard import dashboard_bp
    



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'itwarbazar-server.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'nopviaqsyt'
app.config['MYSQL_PASSWORD'] = 'Malik786'
app.config['MYSQL_DB'] = 'itwarbazar-database'
mysql = MySQL(app)


app.register_blueprint(dashboard_bp)  # Register the blueprint

# User registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_confirm(self, field):
        if self.password.data != field.data:
            raise ValidationError('Passwords must match')

# User login form
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Sign In')

# Routes
@app.route('/')
def home():
    return render_template('home.html')

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
            return redirect(url_for('dashboard.dashboard'))  # Redirect to the dashboard

        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

