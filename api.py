from flask import request, abort
from app import app
from application.master.indexMasterController import *

"""Contain all api for the apps"""

# Bellow is all route for master category product
@app.route('/category_product_api', methods=['GET','POST','PUT', 'DELETE'])
def categoryProductApi():
    if request.method== 'POST':
        return CategoryProductController().insertNewData()
    if request.method=='GET':
        return CategoryProductController().getData()
    if request.method=='PUT':
        return CategoryProductController().updateData()
    if request.method=='DELETE':
        return CategoryProductController().deleteData()

@app.post('/category_product_api_search')
def categoryProductApiSearch():
    return CategoryProductController().searchSingleData()

# Bellow is all route for master company
@app.route('/company_api', methods=['GET','POST','PUT', 'DELETE'])
def companyApi():
    if request.method== 'POST':
        return CompanyController().insertNewData()
    if request.method=='GET':
        return CompanyController().getData()
    if request.method=='PUT':
        return CompanyController().updateData()
    if request.method=='DELETE':
        return CompanyController().deleteData()

@app.post('/company_api_search')
def companyApiSearch():
    return CompanyController().searchSingleData()