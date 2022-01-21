import re
from flask import request
from sqlalchemy import func
from .paymentMethodModel import db,PaymentMethod,PaymentMethodSchema
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler
from application.utilities.response import Response

class PaymentMethodContoller(MasterController):
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
        self.Model=PaymentMethod
        self.Schema=PaymentMethodSchema
        self.parameterHandler=ParameterHandlerImpl()

    def grabLovData(self):
        groupOfObjectResult=self.Model.query.filter(self.Model.mspm_active_status=='Y').all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    def updateData(self, dataFromRequest):
        payment=self.grabOne(dataFromRequest)
        payment.mspm_desc=dataFromRequest.get('mspm_desc')
        payment.mspm_active_status=dataFromRequest.get('mspm_active_status')
        db.session.commit()

    def grabOne(self, paramFromRequest):
        return self.Model.query.filter_by(mspm_id=paramFromRequest.get('mspm_id')).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.mspm_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.mspm_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return self.Model.mspm_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='mspm_id': 
            orderStatement=self.getOrderDirectionById(orderDirection)
        elif columnToOrder=='mspm_desc':
            orderStatement=self.getOrderDirectionByDesc(orderDirection)
        elif columnToOrder=='mspm_active_status':
            orderStatement=self.getOrderDirectionByActiveStatus(orderDirection)
        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mspm_id.desc()
        return self.Model.mspm_id.asc()

    def getOrderDirectionByDesc(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mspm_desc.desc()
        return self.Model.mspm_desc.asc()
    
    def getOrderDirectionByActiveStatus(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mspm_active_status.desc()
        return self.Model.mspm_active_status.asc()
    
class ParameterHandlerImpl(ParameterHandler):
    def getParamInsertFromRequests(self):
        dataFromRequest={
            'mspm_desc':request.json.get('payment_method'),
            'mspm_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest={
            'mspm_id':request.json.get('payment_method_id'),
            'mspm_desc':request.json.get('payment_method'),
            'mspm_active_status':request.json.get('active_status')
        }
        return dataFromRequest

    def getIdFromRequest(self):
        parameterFromRequest={
            'mspm_id':request.json.get('payment_method_id')
        }
        return parameterFromRequest

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='payment_method_id':
            return 'mspm_id'
        if orderColumnName=='payment_method':
            return 'mspm_desc'
        if orderColumnName=='active_status':
            return 'mspm_active_status'
        return None

class ValidationHandlerImpl(ValidationHandler):
    def isParamSearchValid(self, paramFromRequest):
            if not paramFromRequest.get('mspm_id'):
                return False
            return True

    def isParamUpdateValid(self,dataFromRequest):
        if not self.isIdValid(dataFromRequest):
            return False
        if not self.isParamInsertValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        if not self.isPaymentDescValid(dataFromRequest):
            return False
        if not self.isActiveStatusValid(dataFromRequest):
            return False
        return True

    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)


    def isIdValid(self,dataFromRequest):
        if not dataFromRequest.get('mspm_id'):
            return False
        if not self.isNumber(dataFromRequest.get('mspm_id')):
            return False
        return True

    def isPaymentDescValid(self,dataFromRequest):
        if not dataFromRequest.get('mspm_desc'):
            return False
        if len(dataFromRequest.get('mspm_desc'))<3:
            return False
        if len(dataFromRequest.get('mspm_desc'))>200:
            return False
        return True

    def isActiveStatusValid(self,dataFromRequest):
        if not dataFromRequest.get('mspm_active_status'):
            return False
        if not (dataFromRequest.get('mspm_active_status') in ['Y','N']):
            return False
        return True

    def isNumber(self,value):
        # try to parse data to numeric, if work, 
        # then the data is a number.
        try:
            int(value)
        except:
            return False
        return True

    
    