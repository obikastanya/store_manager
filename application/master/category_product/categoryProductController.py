from flask import request
from flask_sqlalchemy.model import Model
from marshmallow.schema import Schema
from .categoryProductModel import db,CategoryProductSchema, CategoryProduct
from sqlalchemy import func
from application.master.baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler

class CategoryProductController(MasterController):
    def __init__(self):
        super().__init__()
        self.dataHandler=DataHandlerImpl()
        self.validationHandler=ValidationHandlerImpl()
        self.parameterHandler=ParameterHandlerImpl()

class DataHandlerImpl(DataHandler):
    def __init__(self):
        super().__init__()
        self.Model=CategoryProduct
        self.Schema=CategoryProductSchema
        self.parameterHandler=ParameterHandlerImpl()
    
    def updateData(self, dataFromRequest):
        categoryProduct=self.grabOne(dataFromRequest)
        categoryProduct.msc_desc=dataFromRequest.get('msc_desc')
        categoryProduct.msc_active_status=dataFromRequest.get('msc_active_status')
        db.session.commit()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.msc_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.msc_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return self.Model.msc_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))

    def grabOne(self,paramFromRequest):
        return self.Model.query.filter_by(msc_id=paramFromRequest.get('msc_id')).first()

    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='msc_id': 
            if orderDirection=='asc':
                orderStatement=self.Model.msc_id.asc()
            if orderDirection=='desc':
                orderStatement=self.Model.msc_id.desc()

        if columnToOrder=='msc_desc':
            if orderDirection=='asc':
                orderStatement=self.Model.msc_desc.asc()
            if orderDirection=='desc':
                orderStatement=self.Model.msc_desc.desc()

        if columnToOrder=='msc_active_status':
            if orderDirection=='asc':
                orderStatement=self.Model.msc_active_status.asc()
            if orderDirection=='desc':
                orderStatement=self.Model.msc_active_status.desc()

        return orderStatement
        

class ParameterHandlerImpl(ParameterHandler):
    # All method bellow is a method to process data and request
    def getValuesFromRequests(self):
        dataFromRequest={
            'msc_desc':request.json.get('category'),
            'msc_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest={
            'msc_desc':request.json.get('category'),
            'msc_active_status':request.json.get('active_status'),
            'msc_id':request.json.get('category_id')
        }
        return dataFromRequest
    def getIdFromRequest(self):
        parameterFromRequest={
            'msc_id':request.json.get('category_id')
        }
        return parameterFromRequest

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='category_id':
            return 'msc_id'
        if orderColumnName=='category':
            return 'msc_desc'
        if orderColumnName=='active_status':
            return 'msc_active_status'
        return None

        
class ValidationHandlerImpl(ValidationHandler):

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
        
    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)

    def isCategoryValid(self,dataFromRequest):
        if not dataFromRequest.get('msc_desc'):
            return False
        if len(dataFromRequest.get('msc_desc'))<3:
            return False
        if len(dataFromRequest.get('msc_desc'))>200:
            return False
        return True