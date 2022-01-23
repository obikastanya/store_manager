from flask import request
from sqlalchemy import func
from .discountModel import db,Discount, DiscountSchema
from ..discount_type.discountTypeModel import DiscountType
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler
from application.utilities.response import Response

class DiscountController(MasterController):
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
        self.Model=Discount
        self.Schema=DiscountSchema
        self.parameterHandler=ParameterHandlerImpl()


    def updateData(self, dataFromRequest):
        discount=self.grabOne(dataFromRequest)
        discount.msd_msdt_id=dataFromRequest.get('msd_msdt_id')
        discount.msd_desc=dataFromRequest.get('msd_desc')
        discount.msd_nominal=dataFromRequest.get('msd_nominal')
        discount.msd_active_status=dataFromRequest.get('msd_active_status')
        db.session.commit()

    def grabLovData(self):
        groupOfObjectResult=self.getQuerySelect().filter(self.Model.msd_active_status=='Y',self.getDefaultFilter() ).all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    def getQuerySelect(self):
        return self.Model.query.join(DiscountType)

    def getDefaultFilter(self):
        return DiscountType.msdt_active_status=='Y'

        
    def grabOne(self, paramFromRequest):
        return self.getQuerySelect().filter(self.Model.msd_id==paramFromRequest.get('msd_id')).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.msd_id)).join(DiscountType).filter(self.getDefaultFilter()).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.msd_id)).join(DiscountType).filter(searchKeyWord,self.getDefaultFilter() ).scalar()

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
    def getParamInsertFromRequests(self):
        dataFromRequest={
            'msd_msdt_id':request.json.get('discount_type'),
            'msd_desc':request.json.get('discount'),
            'msd_nominal':int(request.json.get('nominal',0)),
            'msd_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest={
            'msd_id':request.json.get('discount_id'),
            'msd_msdt_id':request.json.get('discount_type'),
            'msd_desc':request.json.get('discount'),
            'msd_nominal':int(request.json.get('nominal',0)),
            'msd_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getIdFromRequest(self):
        parameterFromRequest={
            'msd_id':request.json.get('discount_id')
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
            if not paramFromRequest.get('msd_id'):
                return False
            return True

    def isParamUpdateValid(self,dataFromRequest):
        if not self.isDiscountIdValid(dataFromRequest):
            return False
        if not self.isParamInsertValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        if not self.isDiscountNameValid(dataFromRequest):
            return False
        if not self.isDiscountTypeValid(dataFromRequest):
            return False
        if not self.isDiscountNominalValid(dataFromRequest):
            return False
        if not self.isValidActiveStatus(dataFromRequest):
            return False
        return True


    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)

    def isDiscountTypeValid(self,dataFromRequest):
        if not dataFromRequest.get('msd_msdt_id'):
            return False
        if not self.isNumber(dataFromRequest.get('msd_msdt_id')):
            return False
        return True

    def isDiscountIdValid(self,dataFromRequest):
        if not dataFromRequest.get('msd_id'):
            return False
        if not self.isNumber(dataFromRequest.get('msd_id')):
            return False
        return True

    def isDiscountNameValid(self,dataFromRequest):
        if not dataFromRequest.get('msd_desc'):
            return False
        if len(dataFromRequest.get('msd_desc'))<3:
            return False
        if len(dataFromRequest.get('msd_desc'))>200:
            return False
        return True

    def isDiscountNominalValid(self,dataFromRequest):
        if not dataFromRequest.get('msd_nominal'):
            return False
        if not self.isNumber(dataFromRequest.get('msd_nominal')):
            return False
        if int(dataFromRequest.get('msd_nominal'))<1:
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
        
    def isValidActiveStatus(self,dataFromRequest):
        if dataFromRequest.get('msd_active_status') not in ['Y','N']:
            return False
        return True
