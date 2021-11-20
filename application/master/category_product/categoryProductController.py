from flask import request
from .categoryProductModel import db,CategoryProductSchema, CategoryProduct
from application.utilities.response import Response

class CategoryProductController:
    # All method bellow is a method whos being called by route function
    def getData(self):
        try:
            categoryProductDatas=DataHandler().callModelAndSchemaToGrabData()
            return Response.make(data=categoryProductDatas)
        except:
            return Response.make(status=False,msg='Eror while trying to retrieve data' )

    def insertNewData(self):
        try:
            dataFromRequest=ParameterHandler().getCategoryFromRequests()
            if not ValidationHandler().isParamInsertValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, insert process has been canceled' )
            DataHandler().callModelToInsertNewData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully added' )
        except:
            return Response.statusAndMsg(False,'Insert data failed' )
    

class ParameterHandler:
    # All method bellow is a method to process data and request
    def getCategoryFromRequests(self):
        dataFromRequest={
            'msc_desc':request.json.get('category'),
            'msc_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest
    

class DataHandler:
    def callModelToInsertNewData(self,dataFromRequest):
        objectToInsert=CategoryProduct(**dataFromRequest)
        db.session.add(objectToInsert)
        db.session.commit()

    def callModelAndSchemaToGrabData(self):
        groupOfObjectResult=CategoryProduct.query.all()
        return CategoryProductSchema(many=True).dump(groupOfObjectResult)
        
class ValidationHandler:
    def isParamInsertValid(self, dataFromRequest):
        if not dataFromRequest.get('msc_desc'):
            return False
        if len(dataFromRequest.get('msc_desc'))<3:
            return False
        if len(dataFromRequest.get('msc_desc'))>200:
            return False
        return True
