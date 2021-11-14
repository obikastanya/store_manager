from os import abort
from flask.wrappers import Request
from flask import request, abort
from app import app
from application.master.baseMaster import *

"""Contain all api for the apps"""
@app.route('/stock_action', methods=['POST','GET'])
def stockApiEndPoint():
    if request.method =='GET':
        return StockController().select()
    if request.method=='POST':
        return StockController().insert()
    abort(404)
