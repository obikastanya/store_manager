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

# master route
@app.get('/category-product')
def categoryProductPage():
    return render_template('master/category_product.html')
@app.get('/company')
def companyPage():
    return render_template('master/company.html')
@app.get('/discount')
def discountPage():
    return render_template('master/discount.html')
    
@app.get('/discount-type')
def discountTypePage():
    return render_template('master/discount_type.html')

@app.get('/employee')
def employeePage():
    return render_template('master/employee.html')

@app.get('/payment-method')
def paymentMethodPage():
    return render_template('master/payment_method.html')

@app.get('/product')
def productPage():
    return render_template('master/product.html')
    