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