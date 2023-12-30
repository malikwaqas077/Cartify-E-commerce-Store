# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField, validators, PasswordField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import ValidationError
 
class ProductForm(FlaskForm):
    name = StringField('Product Name', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    submit = SubmitField('Add Product')
    image = FileField('image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Sign In')