from flask import request
from .categoryProductModel import db,CategoryProductSchema, CategoryProduct
from application.utilities.response import Response

class CategoryProductController:
    # All method bellow is a method whos being called by route function
    def getData(self):
        try:
            categoryProductDatas=DataHandler().grabData()
            return Response.make(data=categoryProductDatas)
        except:
            return Response.make(status=False,msg='Eror while trying to retrieve data' )

    def insertNewData(self):
        try:
            dataFromRequest=ParameterHandler().getCategoryFromRequests()
            if not ValidationHandler().isParamInsertValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, insert process has been canceled' )
            DataHandler().insertNewData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully added' )
        except:
            return Response.statusAndMsg(False,'Insert data failed' )

    def updateData(self):
        try:
            dataFromRequest=ParameterHandler().getUpdatedCategoryFromRequests()
            print(dataFromRequest)
            if not ValidationHandler().isParamUpdateValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, update process has been canceled' )
            DataHandler().updateData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully updated' )
        except:
            return Response.statusAndMsg(False,'update data failed' )

    def searchSingleData(self):
        try:

            paramFromRequest=ParameterHandler().getSearchParameterFromRequest()
            if not ValidationHandler().isParamSearchValid(paramFromRequest):
                return Response.make(False,'Category ID is not valid, process has been canceled' )
            categoryProduct=DataHandler().grabSingleData(paramFromRequest)
            if not DataHandler().isDataExist(categoryProduct):
                return Response.make(False,'Category product is not found' )
            return Response.make(msg='Data Found', data=categoryProduct)
        except:
            return Response.make(False,'Cant find data' )
    

class ParameterHandler:
    # All method bellow is a method to process data and request
    def getCategoryFromRequests(self):
        dataFromRequest={
            'msc_desc':request.json.get('category'),
            'msc_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdatedCategoryFromRequests(self):
        dataFromRequest={
            'msc_desc':request.json.get('category'),
            'msc_active_status':request.json.get('active_status'),
            'msc_id':request.json.get('category_id')
        }
        return dataFromRequest
    def getSearchParameterFromRequest(self):
        parameterFromRequest={
            'msc_id':request.json.get('category_id')
        }
        return parameterFromRequest
    

class DataHandler:
    def insertNewData(self,dataFromRequest):
        objectToInsert=CategoryProduct(**dataFromRequest)
        db.session.add(objectToInsert)
        db.session.commit()

    def grabData(self):
        groupOfObjectResult=CategoryProduct.query.all()
        return CategoryProductSchema(many=True).dump(groupOfObjectResult)
    
    def grabSingleData(self, paramFromRequest):
        groupOfObjectResult=CategoryProduct.query.filter_by(msc_id=paramFromRequest.get('msc_id'))
        return CategoryProductSchema(many=True).dump(groupOfObjectResult)

    def updateData(self, dataFromRequest):
        categoryProduct=CategoryProduct.query.filter_by(msc_id=dataFromRequest.get('msc_id')).first()
        categoryProduct.msc_desc=dataFromRequest.get('msc_desc')
        categoryProduct.msc_active_status=dataFromRequest.get('msc_active_status')
        db.session.commit()

    def isDataExist(self, dataCategoryProduct):
        if(len(dataCategoryProduct)>0):
            return True
        return False

        
        
class ValidationHandler:
    def isCategoryValid(self,dataFromRequest):
        if not dataFromRequest.get('msc_desc'):
            return False
        if len(dataFromRequest.get('msc_desc'))<3:
            return False
        if len(dataFromRequest.get('msc_desc'))>200:
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        return self.isCategoryValid(dataFromRequest)

    def isParamUpdateValid(self,dataFromRequest):
        if not dataFromRequest.get('msc_id'):
            return False
        if not dataFromRequest.get('msc_active_status'):
            return False
        if not  self.isCategoryValid(dataFromRequest):
            return False
        return True

    def isParamSearchValid(self, paramFromRequest):
        if not paramFromRequest.get('msc_id'):
            return False
        return True
