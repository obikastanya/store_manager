from flask import request
from sqlalchemy import func
from .discountModel import db,Discount, DiscountSchema
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler

class DiscountController(MasterController):
    def __init__(self):
        super().__init__()
        self.dataHandler=DataHandlerImpl()
        self.validationHandler=ValidationHandlerImpl()
        self.parameterHandler=ParameterHandlerImpl()

class DataHandlerImpl(DataHandler):
    def __init__(self):
        super().__init__()
        self.Model=Discount
        self.Schema=DiscountSchema
        self.parameterHandler=ParameterHandlerImpl()


    def updateData(self, dataFromRequest):
        pass
        # company=self.grabOne(dataFromRequest)
        # company.mscp_desc=dataFromRequest.get('mscp_desc')
        # company.mscp_active_status=dataFromRequest.get('mscp_active_status')
        # db.session.commit()

    def grabOne(self, paramFromRequest):
        return self.Model.query.filter_by(msd_id=paramFromRequest.get('msd_id')).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.msd_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.msd_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return self.Model.msd_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='msd_id': 
            orderStatement=self.getOrderDirectionById(orderDirection)
        elif columnToOrder=='msd_msdt_id':
            orderStatement=self.getOrderDirectionByTypeId(orderDirection)
        elif columnToOrder=='msd_desc':
            orderStatement=self.getOrderDirectionByDesc(orderDirection)
        elif columnToOrder=='msd_nominal':
            orderStatement=self.getOrderDirectionByNominal(orderDirection)
        elif columnToOrder=='msd_active_status':
            orderStatement=self.getOrderDirectionByActiveStatus(orderDirection)

        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.msd_id.desc()
        return self.Model.msd_id.asc()

    def getOrderDirectionByTypeId(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.msd_msdt_id.desc()
        return self.Model.msd_msdt_id.asc()

    def getOrderDirectionByDesc(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msd_desc.desc()
        return self.Model.msd_desc.asc()

    def getOrderDirectionByNominal(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msd_nominal.desc()
        return self.Model.msd_nominal.asc()

    def getOrderDirectionByActiveStatus(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msd_active_status.desc()
        return self.Model.msd_active_status.asc()

class ParameterHandlerImpl(ParameterHandler):
    def getValuesFromRequests(self):
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
        if orderColumnName=='discount_id':
            return 'msd_id'
        if orderColumnName=='discount':
            return 'msd_desc'
        if orderColumnName=='discount_type':
            return 'msd_msdt_id'
        if orderColumnName=='nominal':
            return 'msd_nominal'
        if orderColumnName=='active_status':
            return 'msd_active_status'
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