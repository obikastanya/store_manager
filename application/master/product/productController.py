from flask import request
from sqlalchemy import func
from .productModel import db,Product, ProductSchema
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler


class ProductController(MasterController):
    def __init__(self):
        super().__init__()
        self.dataHandler=DataHandlerImpl()
        self.validationHandler=ValidationHandlerImpl()
        self.parameterHandler=ParameterHandlerImpl()

class DataHandlerImpl(DataHandler):
    def __init__(self):
        super().__init__()
        self.Model=Product
        self.Schema=ProductSchema
        self.parameterHandler=ParameterHandlerImpl()


    def updateData(self, dataFromRequest):
        product=self.grabOne(dataFromRequest)
        product.msp_brand=dataFromRequest.get('msp_brand')
        product.msp_msc_id=dataFromRequest.get('msp_msc_id')
        product.msp_price=dataFromRequest.get('msp_price')
        product.msp_mssp_id=dataFromRequest.get('msp_mssp_id')
        product.msp_mscp_id=dataFromRequest.get('msp_mscp_id')
        product.msp_active_status=dataFromRequest.get('msp_active_status')
        db.session.commit()

    def grabOne(self, paramFromRequest):
        return self.Model.query.filter_by(msp_id=paramFromRequest.get('msp_id')).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.msp_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.msp_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return self.Model.msp_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='msp_id': 
            orderStatement=self.getOrderDirectionById(orderDirection)
        elif columnToOrder=='msp_brand':
            orderStatement=self.getOrderDirectionByBrand(orderDirection)
        elif columnToOrder=='msp_msc_id':
            orderStatement=self.getOrderDirectionByCategoryId(orderDirection)
        elif columnToOrder=='msp_price':
            orderStatement=self.getOrderDirectionByPrice(orderDirection)
        elif columnToOrder=='msp_desc':
            orderStatement=self.getOrderDirectionByDesc(orderDirection)
        elif columnToOrder=='msp_mssp_id':
            orderStatement=self.getOrderDirectionBySupplier(orderDirection)
        elif columnToOrder=='msp_mscp_id':
            orderStatement=self.getOrderDirectionByCompany(orderDirection)
        elif columnToOrder=='msp_active_status':
            orderStatement=self.getOrderDirectionByActiveStatus(orderDirection)
        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.msp_id.desc()
        return self.Model.msp_id.asc()
    
    def getOrderDirectionByBrand(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.msp_brand.desc()
        return self.Model.msp_brand.asc()

    def getOrderDirectionByCategoryId(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msp_msc_id.desc()
        return self.Model.msp_msc_id.asc()

    def getOrderDirectionByPrice(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msp_price.desc()
        return self.Model.msp_price.asc()

    def getOrderDirectionByDesc(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msp_desc.desc()
        return self.Model.msp_desc.asc()

    def getOrderDirectionBySupplier(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msp_mssp_id.desc()
        return self.Model.msp_mssp_id.asc()

    def getOrderDirectionByCompany(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msp_mscp_id.desc()
        return self.Model.msp_mscp_id.asc()
        

    def getOrderDirectionByActiveStatus(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.msp_active_status.desc()
        return self.Model.msp_active_status.asc()

class ParameterHandlerImpl(ParameterHandler):
    def getParamInsertFromRequests(self):
        dataFromRequest={
            'msp_desc':request.json.get('product_desc'),
            'msp_brand':request.json.get('brand'),
            'msp_price':request.json.get('price',0),
            'msp_msc_id':request.json.get('category'),
            'msp_mssp_id':request.json.get('supplier'),
            'msp_mscp_id':request.json.get('company'),
            'msp_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest={
            'msp_id':request.json.get('product_id'),
            'msp_desc':request.json.get('product_desc'),
            'msp_brand':request.json.get('brand'),
            'msp_price':request.json.get('price',0),
            'msp_msc_id':request.json.get('category'),
            'msp_mssp_id':request.json.get('supplier'),
            'msp_mscp_id':request.json.get('company'),
            'msp_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getIdFromRequest(self):
        parameterFromRequest={
            'msp_id':request.json.get('product_id')
        }
        return parameterFromRequest

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='product_id':
            return 'msp_id'
        if orderColumnName=='product_desc':
            return 'msp_desc'
        if orderColumnName=='brand':
            return 'msp_brand'
        if orderColumnName=='price':
            return 'msp_price'
        if orderColumnName=='category':
            return 'msp_msc_id'
        if orderColumnName=='supplier':
            return 'msp_mssp_id'
        if orderColumnName=='company':
            return 'msp_mscp_id'
        if orderColumnName=='active_status':
            return 'msp_active_status'
        return None

class ValidationHandlerImpl(ValidationHandler):
    def isParamSearchValid(self, dataFromRequest):
            if not dataFromRequest.get('msp_id'):
                return False
            return True

    def isParamUpdateValid(self,dataFromRequest):
        if not self.isProductIdValid(dataFromRequest):
            return False
        if not self.isParamInsertValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        if not self.isProductDescValid(dataFromRequest):
            return False
        if not self.isBrandValid(dataFromRequest):
            return False
        if not self.isPriceValid(dataFromRequest):
            return False
        if not self.isCategoryIdValid(dataFromRequest):
            return False
        if not self.isSupplierIdValid(dataFromRequest):
            return False
        if not self.isCompanyIdValid(dataFromRequest):
            return False
        if not self.isActiveStatusValid(dataFromRequest):
            return False
        return True


    def isParamDeleteValid(self, dataFromRequest):
        return self.isParamSearchValid(dataFromRequest)

    def isProductDescValid(self,dataFromRequest):
        if not dataFromRequest.get('msp_desc'):
            return False
        if len(dataFromRequest.get('msp_desc'))<3:
            return False
        if len(dataFromRequest.get('msp_desc'))>500:
            return False
        return True

    def isBrandValid(self,dataFromRequest):
        if not dataFromRequest.get('msp_brand'):
            return False
        if len(dataFromRequest.get('msp_desc'))<3:
            return False
        if len(dataFromRequest.get('msp_desc'))>100:
            return False
        return True

    def isPriceValid(self,dataFromRequest):
        if not dataFromRequest.get('msp_price'):
            return False
        if not self.isNumber(dataFromRequest.get('msp_price')):
            return False
        if int(dataFromRequest.get('msp_price'))<1:
            return False
        if len(str(dataFromRequest.get('msp_price')))>12:
            return False
        return True

    def isCategoryIdValid(self, dataFromRequest):
        if not dataFromRequest.get('msp_msc_id'):
            return False
        if not self.isNumber(dataFromRequest.get('msp_msc_id')):
            return False
        return True

    def isSupplierIdValid(self,dataFromRequest):
        if not dataFromRequest.get('msp_mssp_id'):
            return False
        if not self.isNumber(dataFromRequest.get('msp_mssp_id')):
            return False
        return True

    def isProductIdValid(self,dataFromRequest):
        if not dataFromRequest.get('msp_id'):
            return False
        if not self.isNumber(dataFromRequest.get('msp_id')):
            return False
        return True

    def isCompanyIdValid(self,dataFromRequest):
        if not dataFromRequest.get('msp_mscp_id'):
            return False
        if not self.isNumber(dataFromRequest.get('msp_mscp_id')):
            return False
        return True

    def isActiveStatusValid(self,dataFromRequest):
        if not dataFromRequest.get('msp_active_status'):
            return False
        if dataFromRequest.get('msp_active_status') not in ['N','Y']:
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

