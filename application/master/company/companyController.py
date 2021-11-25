from flask import request

from application.master.category_product.categoryProductController import DataHandler
from .companyModel import db,Company, CompanySchema
from application.utilities.response import Response

class CompanyController:
    def insert(self):
        data=Company(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def getData(self):
        try:
            limit,offset=ParameterHandler().getOffsetLimit()
            if not ValidationHandler().isValidLimitOffset(limit,offset):
                return Response.make(status=False,msg='Invalid page size detected, cant show data')
            companyData=DataHandler().grabData()

            return Response.make(data=companyData)
        except:
            return Response.make(status=False, msg='Eror while trying to retrieve data' )
        
    

class ParameterHandler:
    # All method bellow is a method to process data and request
    def getOffsetLimit(self):
        offset=request.args.get('start',0)
        limit=request.args.get('length',10)
        return limit,offset

class DataHandler:
    def grabData(self):
        limit,offset=ParameterHandler().getOffsetLimit()
        groupOfResult=Company.query.offset(offset).limit(limit).all()
        return CompanySchema(many=True).dump(groupOfResult)
    # handle SQL Alchemy Process
        
        
class ValidationHandler:
    def isValidLimitOffset(self, limit,offset):
        if limit=='' or offset=='':
            return False
        return True
    # Handle validation