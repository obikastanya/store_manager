from flask import render_template
from app import app
@app.route('/')
def dashboardPage():
    return render_template('dashboard.html')

@app.route('/product-sold')
def productSoldPage():
    return render_template('product_sold.html')

@app.route('/product-purchased')
def productPurchasedPage():
    return render_template('product_purchased.html')

@app.route('/manage-discount')
def manageDiscountPage():
    return render_template('manage_discount.html')

@app.route('/report')
def reportPage():
    return render_template('report.html')

