from flask import request
from sqlalchemy import func
from application.utilities.response import Response
from .discountTypeModel import db,DiscountType, DiscountTypeSchema
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler

class DiscountTypeController(MasterController):
    # this class doesnt allowing any operation except select to master discount type, 
    # the data is static
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

    def insertNewData(self):
        return self.makeInvalidOperation()
    def updateData(self):
        return self.makeInvalidOperation()
    def deleteData(self):
        return self.makeInvalidOperation()
    def searchSingleData(self):
        return self.makeInvalidOperation()
    def makeInvalidOperation(self):
        return Response.statusAndMsg(False,'Cant perform this operation')

class DataHandlerImpl(DataHandler):
    def __init__(self):
        super().__init__()
        self.Model=DiscountType
        self.Schema=DiscountTypeSchema
        self.parameterHandler=ParameterHandlerImpl()

    def grabOne(self, paramFromRequest):
        return self.Model.query.filter_by(msdt_id=paramFromRequest.get('msdt_id')).first()

    def grabLovData(self):
        groupOfObjectResult=self.Model.query.filter(self.Model.msdt_active_status=="Y").all()
        return self.Schema(many=True).dump(groupOfObjectResult)
        
    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.msdt_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.msdt_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return self.Model.msdt_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='msdt_id': 
            orderStatement=self.getOrderDirectionById(orderDirection)
        elif columnToOrder=='msdt_desc':
            orderStatement=self.getOrderDirectionByDesc(orderDirection)
        elif columnToOrder=='msdt_active_status':
            orderStatement=self.getOrderDirectionByActiveStatus(orderDirection)
        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.msdt_id.desc()
        return self.Model.msdt_id.asc()

    def getOrderDirectionByDesc(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msdt_desc.desc()
        return self.Model.msdt_desc.asc()

    def getOrderDirectionByActiveStatus(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msdt_active_status.desc()
        return self.Model.msdt_active_status.asc()

class ParameterHandlerImpl(ParameterHandler):
    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='discount_type_id':
            return 'msdt_id'
        if orderColumnName=='discount_type':
            return 'msdt_desc'
        if orderColumnName=='active_status':
            return 'msdt_active_status'
        return None

class ValidationHandlerImpl(ValidationHandler):
    def __init__(self):
        super().__init__()

