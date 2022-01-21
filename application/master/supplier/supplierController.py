from datetime import date
from flask import request
from sqlalchemy import func
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler
from .supplierModel import db,Supplier, SupplierSchema
from application.utilities.response import Response

class SupplierController(MasterController):
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
        self.Model=Supplier
        self.Schema=SupplierSchema
        self.parameterHandler=ParameterHandlerImpl()


    def updateData(self, dataFromRequest):
        supplier=self.grabOne(dataFromRequest)
        supplier.mssp_desc=dataFromRequest.get('mssp_desc')
        supplier.mssp_phone_number=dataFromRequest.get('mssp_phone_number')
        supplier.mssp_address=dataFromRequest.get('mssp_address')
        supplier.mssp_active_status=dataFromRequest.get('mssp_active_status')
        db.session.commit()

    def grabLovData(self):
        groupOfObjectResult=self.Model.query.filter(self.Model.mssp_active_status=='Y').all()
        return self.Schema(many=True).dump(groupOfObjectResult)
        
    def grabOne(self, paramFromRequest):
        return self.Model.query.filter_by(mssp_id=paramFromRequest.get('mssp_id')).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.mssp_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.mssp_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return self.Model.mssp_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='mssp_id': 
            orderStatement=self.getOrderDirectionById(orderDirection)
        elif columnToOrder=='mssp_desc':
            orderStatement=self.getOrderDirectionByDesc(orderDirection)
        elif columnToOrder=='mssp_phone_number':
            orderStatement=self.getOrderDirectionByPhoneNumber(orderDirection)
        elif columnToOrder=='mssp_address':
            orderStatement=self.getOrderDirectionByAddress(orderDirection)
        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mssp_id.desc()
        return self.Model.mssp_id.asc()

    def getOrderDirectionByDesc(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.mssp_desc.desc()
        return self.Model.mssp_desc.asc()

    def getOrderDirectionByPhoneNumber(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.mssp_address.desc()
        return self.Model.mssp_address.asc()

    def getOrderDirectionByAddress(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mssp_address.desc()
        return self.Model.mssp_address.asc()
    
    def getOrderDirectionByActiveStatus(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mssp_active_status.desc()
        return self.Model.mssp_active_status.asc()

class ParameterHandlerImpl(ParameterHandler):
    def getParamInsertFromRequests(self):
        dataFromRequest={
            'mssp_desc':request.json.get('supplier'),
            'mssp_phone_number':request.json.get('phone_number'),
            'mssp_address':request.json.get('address'),
            'mssp_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest={
            'mssp_id':request.json.get('supplier_id'),
            'mssp_desc':request.json.get('supplier'),
            'mssp_phone_number':request.json.get('phone_number'),
            'mssp_address':request.json.get('address'),
            'mssp_active_status':request.json.get('active_status')
        }
        return dataFromRequest

    def getIdFromRequest(self):
        parameterFromRequest={
            'mssp_id':request.json.get('supplier_id')
        }
        return parameterFromRequest

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='supplier_id':
            return 'mssp_id'
        if orderColumnName=='supplier':
            return 'mssp_desc'
        if orderColumnName=='phone_number':
            return 'mssp_phone_number'
        if orderColumnName=='address':
            return 'mssp_address'
        if orderColumnName=='active_status':
            return 'mssp_active_status'
        return None

class ValidationHandlerImpl(ValidationHandler):
    def isParamSearchValid(self, paramFromRequest):
            if not paramFromRequest.get('mssp_id'):
                return False
            return True

    def isParamUpdateValid(self,dataFromRequest):
        if not self.isValidIdSupplier(dataFromRequest.get('mssp_id')):
            return False
        if not self.isParamInsertValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        if not self.isValidSupplierDesc(dataFromRequest.get('mssp_desc')):
            return False
        if not self.isValidPhoneNumber(dataFromRequest.get('mssp_phone_number')):
            return False
        if not self.isValidAddress(dataFromRequest.get('mssp_address')):
            return False
        if not self.isValidActiveStatus(dataFromRequest.get('mssp_active_status')):
            return False
        return True

    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)
    
    def isValidIdSupplier(self,supplierId):
        if not supplierId:
            return False
        if not self.isNumber(supplierId):
            return False
        return True

    def isValidSupplierDesc(self,supplierDesc):
        if not supplierDesc:
            return False
        if len(supplierDesc)<3:
            return False
        if len(supplierDesc)>200:
            return False
        return True
    def isValidPhoneNumber(self,phoneNumber):
        if not phoneNumber:
            return False
        if len(str(phoneNumber))<3:
            return False
        if len(str(phoneNumber))>15:
            return False
        return True
    def isValidAddress(self,address):
        if not address:
            return False
        if len(address)<5:
            return False
        if len(address)>300:
            return False
        return True
    def isValidActiveStatus(self,activeStatus):
        if not activeStatus:
            return False
        if activeStatus not in ['Y','N']:
            return False
        return True

    def isNumber(self,value):
        try:
            int(value)
        except:
            return False
        return True