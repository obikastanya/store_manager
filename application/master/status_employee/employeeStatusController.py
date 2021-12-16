from flask import request
from sqlalchemy import func
from .employeeStatusModel import db,StatusEmployee, StatusEmployeeSchema
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler

class EmployeeStatusController(MasterController):
    def __init__(self):
        super().__init__()
        self.dataHandler=DataHandlerImpl()
        self.validationHandler=ValidationHandlerImpl()
        self.parameterHandler=ParameterHandlerImpl()

class DataHandlerImpl(DataHandler):
    def __init__(self):
        super().__init__()
        self.Model=StatusEmployee
        self.Schema=StatusEmployeeSchema
        self.parameterHandler=ParameterHandlerImpl()


    def updateData(self, dataFromRequest):
        employeeStatus=self.grabOne(dataFromRequest)
        employeeStatus.msse_desc=dataFromRequest.get('msee_desc')
        employeeStatus.msse_active_status=dataFromRequest.get('msse_active_status')
        db.session.commit()

    def grabOne(self, paramFromRequest):
        return self.Model.query.filter_by(msse_id=paramFromRequest.get('msse_id')).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.msse_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.msse_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return self.Model.msse_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='msse_id': 
            orderStatement=self.getOrderDirectionById(orderDirection)
        elif columnToOrder=='msse_desc':
            orderStatement=self.getOrderDirectionByDesc(orderDirection)
        elif columnToOrder=='msse_active_status':
            orderStatement=self.getOrderDirectionByActiveStatus(orderDirection)

        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.msse_id.desc()
        return self.Model.msse_id.asc()

    def getOrderDirectionByDesc(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msse_desc.desc()
        return self.Model.msse_desc.asc()

    def getOrderDirectionByActiveStatus(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msse_active_status.desc()
        return self.Model.msse_active_status.asc()

class ParameterHandlerImpl(ParameterHandler):
    def getParamInsertFromRequests(self):
        dataFromRequest={
            'msse_desc':request.json.get('employee_status'),
            'msse_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest={
            'msse_desc':request.json.get('employee_status'),
            'msse_id':request.json.get('employee_status_id'),
            'msse_active_status':request.json.get('active_status')
        }
        return dataFromRequest

    def getIdFromRequest(self):
        parameterFromRequest={
            'msse_id':request.json.get('employee_status_id')
        }
        return parameterFromRequest

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='employee_status_id':
            return 'msse_id'
        if orderColumnName=='employee_status':
            return 'msse_desc'
        if orderColumnName=='active_status':
            return 'msse_active_status'
        return None

class ValidationHandlerImpl(ValidationHandler):
    def isParamSearchValid(self, paramFromRequest):
        if not paramFromRequest.get('msse_id'):
            return False
        return True

    def isParamUpdateValid(self,dataFromRequest):
        if not dataFromRequest.get('msse_id'):
            return False
        if not dataFromRequest.get('msse_active_status'):
            return False
        if not  self.isEmployeeStatusValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        return self.isEmployeeStatusValid(dataFromRequest)

    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)

    def isEmployeeStatusValid(self,dataFromRequest):
        if not dataFromRequest.get('msse_desc'):
            return False
        if len(dataFromRequest.get('msse_desc'))<3:
            return False
        if len(dataFromRequest.get('msse_desc'))>200:
            return False
        return True

