# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField, validators
from flask_wtf.file import FileField, FileAllowed
class ProductForm(FlaskForm):
    name = StringField('Product Name', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    submit = SubmitField('Add Product')
    image = FileField('image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

