from flask import request
from sqlalchemy import func
from .categoryProductModel import db,CategoryProductSchema, CategoryProduct
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler
from application.utilities.response import Response

class CategoryProductController(MasterController):
    def __init__(self):
        super().__init__()
        self.dataHandler=DataHandlerImpl()
        self.validationHandler=ValidationHandlerImpl()
        self.parameterHandler=ParameterHandlerImpl()

    def getLovData(self):
        try:
            data=self.dataHandler.grabLovData()
            return Response.make(msg='Data found',data=data)
        except:
            return Response.make(status=False,msg='Eror while trying to retrieve data' )

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
        
    def grabLovData(self):
        groupOfObjectResult=self.Model.query.filter(self.Model.msc_active_status=='Y').all()
        return self.Schema(many=True).dump(groupOfObjectResult)

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
            orderStatement=self.getOrderDirectionById(orderDirection)
        elif columnToOrder=='msc_desc':
            orderStatement=self.getOrderDirectionByDesc(orderDirection)
        elif columnToOrder=='msc_active_status':
            orderStatement=self.getOrderDirectionByActiveStatus(orderDirection)

        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.msc_id.desc()
        return self.Model.msc_id.asc()

    def getOrderDirectionByDesc(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msc_desc.desc()
        return self.Model.msc_desc.asc()

    def getOrderDirectionByActiveStatus(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msc_active_status.desc()
        return self.Model.msc_active_status.asc()
        

class ParameterHandlerImpl(ParameterHandler):
    # All method bellow is a method to process data and request
    def getParamInsertFromRequests(self):
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