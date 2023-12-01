# product_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from forms import ProductForm
from models import db, Product

product_bp = Blueprint('product', __name__, template_folder='templates')

@product_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('product.add_product'))

    return render_template('add_product.html', form=form)
