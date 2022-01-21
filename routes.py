from flask import render_template, request
from app import app
from application.auth.authController import Auth

@app.post('/login')
def loginAuth():
    try:    
        return Auth().checkAccess()
    except:
        msg="Login Failed"
        return render_template('login.html', msg=msg)


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

@app.get('/employee-status')
def employeeStatusPage():
    return render_template('master/employee_status.html')

@app.get('/stock')
def stockPage():
    return render_template('master/stock.html')

@app.get('/supplier')
def supplierPage():
    return render_template('master/supplier.html')
    
@app.get('/login')
def loginPage():
    return render_template('login.html')

@app.get('/logout')
def logoutPage():
    Auth().logOut()
    return render_template('login.html')
