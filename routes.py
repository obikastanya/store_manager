from flask import render_template, request
import jwt
from app import app
from application.auth.authController import Auth, AuthToken

authToken=AuthToken()

"""Contain all route that return html as responses"""

@app.post('/login')
def loginAuth(**kwargs):
    try:    
        return Auth().checkAccess()
    except:
        msg="Login Failed"
        return render_template('login.html', msg=msg)

@app.get('/login')
def loginPage():
    return render_template('login.html')

@app.get('/')
@authToken.authenticate
def dashboardPage(**kwargs):
    print(kwargs)
    return render_template('dashboard.html')

@app.get('/product-sold')
@authToken.authenticate
def productSoldPage(**kwargs):
    return render_template('product_sold.html')

@app.get('/product-purchased')
@authToken.authenticate
def productPurchasedPage(**kwargs):
    return render_template('product_purchased.html')

@app.get('/manage-discount')
@authToken.authenticate
def manageDiscountPage(**kwargs):
    return render_template('manage_discount.html')

@app.get('/report')
@authToken.authenticate
def reportPage(**kwargs):
    return render_template('report.html')

# master route
@app.get('/category-product')
@authToken.authenticate
def categoryProductPage(**kwargs):
    return render_template('master/category_product.html')

@app.get('/company')
@authToken.authenticate
def companyPage(**kwargs):
    return render_template('master/company.html')

@app.get('/discount')
@authToken.authenticate
def discountPage(**kwargs):
    return render_template('master/discount.html')
    
@app.get('/discount-type')
@authToken.authenticate
def discountTypePage(**kwargs):
    return render_template('master/discount_type.html')

@app.get('/employee')
@authToken.authenticate
def employeePage(**kwargs):
    return render_template('master/employee.html')

@app.get('/payment-method')
@authToken.authenticate
def paymentMethodPage(**kwargs):
    return render_template('master/payment_method.html')

@app.get('/product')
@authToken.authenticate
def productPage(**kwargs):
    return render_template('master/product.html')

@app.get('/employee-status')
@authToken.authenticate
def employeeStatusPage(**kwargs):
    return render_template('master/employee_status.html')

@app.get('/stock')
@authToken.authenticate
def stockPage(**kwargs):
    return render_template('master/stock.html')

@app.get('/supplier')
@authToken.authenticate
def supplierPage(**kwargs):
    return render_template('master/supplier.html')

@app.get('/logout')
@authToken.authenticate
def logoutPage(**kwargs):
    return Auth().logOut()
