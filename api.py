from flask import request, abort
from app import app
from application.master.indexMasterController import *

def splitRouteByMethods(Controller):
    if request.method== 'POST':
        return Controller().insertNewData()
    if request.method=='GET':
        return Controller().getData()
    if request.method=='PUT':
        return Controller().updateData()
    if request.method=='DELETE':
        return Controller().deleteData()

"""Contain all api for the apps"""
# Bellow is all route for master category product
@app.route('/category_product_api', methods=['GET','POST','PUT', 'DELETE'])
def categoryProductApi():
    return splitRouteByMethods(CategoryProductController)

@app.post('/category_product_api_search')
def categoryProductApiSearch():
    return CategoryProductController().searchSingleData()

# Bellow is all route for master company
@app.route('/company_api', methods=['GET','POST','PUT', 'DELETE'])
def companyApi():
    return splitRouteByMethods(CompanyController)

@app.post('/company_api_search')
def companyApiSearch():
    return CompanyController().searchSingleData()

# bellow is all route for master discount 
@app.route('/discount_api',methods=['GET','POST','PUT', 'DELETE'])
def discountApi():
    return splitRouteByMethods(DiscountController)

@app.post('/discount_api_search')
def discountApiSearch():
    return DiscountController().searchSingleData()

# bellow is all route for master discount 
@app.route('/discount_type_api',methods=['GET','POST','PUT', 'DELETE'])
def discountTypeApi():
    return splitRouteByMethods(DiscountTypeController)

@app.post('/discount_type_api_search')
def discountTypeApiSearch():
    return DiscountController().searchSingleData()

@app.route('/employee_api',methods=['GET','POST','PUT', 'DELETE'])
def employeeApi():
    return splitRouteByMethods(EmployeeController)

@app.post('/employee_api_search')
def employeeApiSearch():
    return EmployeeController().searchSingleData()

@app.route('/payment_method_api',methods=['GET','POST','PUT', 'DELETE'])
def paymentMethodApi():
    return splitRouteByMethods(PaymentMethodContoller)
    
@app.post('/payment_method_api_search')
def paymentMethodApiSearch():
    return PaymentMethodContoller().searchSingleData()

@app.route('/product_api',methods=['GET','POST','PUT', 'DELETE'])
def productApi():
    return splitRouteByMethods(ProductController)
    
@app.post('/product_api_search')
def productApiSearch():
    return ProductController().searchSingleData()

@app.route('/employee_status_api',methods=['GET','POST','PUT', 'DELETE'])
def employeeStatusApi():
    return splitRouteByMethods(EmployeeStatusController)
    
@app.post('/employee_status_api_search')
def employeeStatusApiSearch():
    return EmployeeStatusController().searchSingleData()

@app.route('/stock_api',methods=['GET','POST','PUT', 'DELETE'])
def stockApi():
    return splitRouteByMethods(StockController)
    
@app.post('/stock_api_search')
def stockApiSearch():
    return StockController().searchSingleData()

@app.route('/supplier_api',methods=['GET','POST','PUT', 'DELETE'])
def supplierApi():
    return splitRouteByMethods(SupplierController)
    
@app.post('/supplier_api_search')
def supplierApiSearch():
    return SupplierController().searchSingleData()

# Lov Api End Point
@app.post('/supplier_lov_api')
def supplierLovApi():
    return SupplierController().getLovData()

@app.post('/discount_type_lov_api')
def discountTypeLovApi():
    return DiscountTypeController().getLovData()

@app.post('/category_product_lov_api')
def categoryProductLovApi():
    return CategoryProductController().getLovData()

@app.post('/company_lov_api')
def companyLovApi():
    return CompanyController().getLovData()
