from flask import request
from sqlalchemy import func
from .companyModel import db,Company, CompanySchema
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler

class CompanyController(MasterController):
    def __init__(self):
        super().__init__()
        self.dataHandler=DataHandlerImpl()
        self.validationHandler=ValidationHandlerImpl()
        self.parameterHandler=ParameterHandlerImpl()

class DataHandlerImpl(DataHandler):
    def __init__(self):
        super().__init__()
        self.Model=Company
        self.Schema=CompanySchema
        self.parameterHandler=ParameterHandlerImpl()


    def updateData(self, dataFromRequest):
        company=self.grabOne(dataFromRequest)
        company.mscp_desc=dataFromRequest.get('mscp_desc')
        company.mscp_active_status=dataFromRequest.get('mscp_active_status')
        db.session.commit()

    def grabOne(self, paramFromRequest):
        return self.Model.query.filter_by(mscp_id=paramFromRequest.get('mscp_id')).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.mscp_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.mscp_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return self.Model.mscp_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='mscp_id': 
            orderStatement=self.getOrderDirectionById(orderDirection)
        elif columnToOrder=='mscp_desc':
            orderStatement=self.getOrderDirectionByDesc(orderDirection)
        elif columnToOrder=='mscp_active_status':
            orderStatement=self.getOrderDirectionByActiveStatus(orderDirection)

        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mscp_id.desc()
        return self.Model.mscp_id.asc()

    def getOrderDirectionByDesc(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.mscp_desc.desc()
        return self.Model.mscp_desc.asc()

    def getOrderDirectionByActiveStatus(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.mscp_active_status.desc()
        return self.Model.mscp_active_status.asc()

class ParameterHandlerImpl(ParameterHandler):
    def getParamInsertFromRequests(self):
        dataFromRequest={
            'mscp_desc':request.json.get('company'),
            'mscp_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest={
            'mscp_desc':request.json.get('company'),
            'mscp_active_status':request.json.get('active_status'),
            'mscp_id':request.json.get('company_id')
        }
        return dataFromRequest

    def getIdFromRequest(self):
        parameterFromRequest={
            'mscp_id':request.json.get('company_id')
        }
        return parameterFromRequest

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='company_id':
            return 'mscp_id'
        if orderColumnName=='company':
            return 'mscp_desc'
        if orderColumnName=='active_status':
            return 'mscp_active_status'
        return None

class ValidationHandlerImpl(ValidationHandler):
    def isParamSearchValid(self, paramFromRequest):
            if not paramFromRequest.get('mscp_id'):
                return False
            return True

    def isParamUpdateValid(self,dataFromRequest):
        if not dataFromRequest.get('mscp_id'):
            return False
        if not dataFromRequest.get('mscp_active_status'):
            return False
        if not  self.isCompanyValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        return self.isCompanyValid(dataFromRequest)

    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)

    def isCompanyValid(self,dataFromRequest):
        if not dataFromRequest.get('mscp_desc'):
            return False
        if len(dataFromRequest.get('mscp_desc'))<3:
            return False
        if len(dataFromRequest.get('mscp_desc'))>200:
            return False
        return True