from flask import request, abort
from app import app
from application.master.baseMaster import *

"""Contain all api for the apps"""

# Bellow is all route for master category product
@app.route('/category_product_api', methods=['GET','POST'])
def categoryProductApi():
    if request.method== 'POST':
        return CategoryProductController().insertNewData()
    if request.method=='GET':
        return CategoryProductController().getData()

