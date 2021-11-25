from flask import render_template
from app import app

"""Contain all route that return html as responses"""
@app.get('/')
def dashboardPage():
    return render_template('dashboard.html')

@app.get('/product-sold')
def productSoldPage():
    return render_template('product_sold.html')

@app.get('/product-purchased')
def productPurchasedPage():
    return render_template('product_purchased.html')

@app.get('/manage-discount')
def manageDiscountPage():
    return render_template('manage_discount.html')

@app.get('/report')
def reportPage():
    return render_template('report.html')

@app.get('/category-product')
def companyPage():
    return render_template('master/category_product.html')
@app.get('/company')
def categoryProductPage():
    return render_template('master/company.html')