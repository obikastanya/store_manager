from flask import request
from flask_sqlalchemy.model import Model
from sqlalchemy import func
from ..master.baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler
from .manageDiscountModel import db, ManageDiscount, ManageDiscountSchema
from ..master.product.productModel import Product
from ..master.discount.discountModel import Discount
from ..master.discount_type.discountTypeModel import DiscountType


class ManageDiscountController(MasterController):
    def __init__(self):
        super().__init__()
        self.dataHandler = DataHandlerImpl()
        self.validationHandler = ValidationHandlerImpl()
        self.parameterHandler = ParameterHandlerImpl()


class DataHandlerImpl(DataHandler):
    def __init__(self):
        super().__init__()
        self.Model = ManageDiscount
        self.Schema = ManageDiscountSchema
        self.parameterHandler = ParameterHandlerImpl()

    def updateData(self, dataFromRequest):
        discountApplied = self.grabOne(dataFromRequest)
        discountApplied.da_start_date = dataFromRequest.get('da_start_date')
        discountApplied.da_expired_date = dataFromRequest.get(
            'da_expired_date')
        discountApplied.da_active_status = dataFromRequest.get(
            'da_active_status')
        db.session.commit()

    def grabDataWithKeywordAndOrder(self,datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=db.session.query(self.Model).join(Product).join(Discount).join(DiscountType).filter(searchKeyWord).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    
    def grabDataWithKeyword(self,datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=db.session.query(self.Model).join(Product).filter(searchKeyWord).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)
    
    def grabDataWithOrderby(self, datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=db.session.query(self.Model).join(Product).join(Discount).join(DiscountType).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    def grabOne(self, paramFromRequest):
        return self.Model.query.filter(
            (self.Model.da_msp_id == paramFromRequest.get('da_msp_id'))
            & (self.Model.da_msd_id == paramFromRequest.get('da_msd_id'))
        ).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.da_msp_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord = self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(
            self.Model.da_msp_id)).filter(searchKeyWord).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return Product.msp_desc.like("%{}%".format(
            datatableConfig.get('searchKeyWord')))

    def getOrderStatement(self, datatableConfig):
        orderStatement = None
        columnToOrder = datatableConfig.get('orderBy')
        orderDirection = datatableConfig.get('orderDirection')

        if columnToOrder == 'da_msp_id':
            orderStatement = self.getOrderDirectionById(orderDirection)
        if columnToOrder == 'msp_desc':
            orderStatement = self.getOrderDirectionByProductDesc(orderDirection)
        if columnToOrder == 'msd_desc':
            orderStatement = self.getOrderDirectionByDiscount(orderDirection)
        if columnToOrder == 'msdt_desc':
            orderStatement = self.getOrderDirectionByDiscountType(orderDirection)
        if columnToOrder == 'da_start_date':
            orderStatement = self.getOrderDirectionByStartDate(orderDirection)
        if columnToOrder == 'da_expired_date':
            orderStatement = self.getOrderDirectionByExpiredDate(orderDirection)
        elif columnToOrder == 'da_active_status':
            orderStatement = self.getOrderDirectionByActiveStatus(
                orderDirection)
        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection == 'desc':
            return self.Model.da_msp_id.desc()
        return self.Model.da_msp_id.asc()
    
    def getOrderDirectionByProductDesc(self,orderDirection):
        if orderDirection == 'desc':
            return Product.msp_desc.desc()
        return Product.msp_desc.asc()
    
    def getOrderDirectionByDiscount(self,orderDirection):
        if orderDirection == 'desc':
            return Discount.msd_desc.desc()
        return Discount.msd_desc.asc()
    
    def getOrderDirectionByDiscountType(self,orderDirection):
        if orderDirection == 'desc':
            return DiscountType.msdt_desc.desc()
        return DiscountType.msdt_desc.asc()
    
    def getOrderDirectionByStartDate(self,orderDirection):
        if orderDirection == 'desc':
            return self.Model.da_start_date.desc()
        return self.Model.da_start_date.asc()
    
    def getOrderDirectionByExpiredDate(self,orderDirection):
        if orderDirection == 'desc':
            return self.Model.da_expired_date.desc()
        return self.Model.da_expired_date.asc()

    def getOrderDirectionByActiveStatus(self, orderDirection):
        if orderDirection == 'desc':
            return self.Model.da_active_status.desc()
        return self.Model.da_active_status.asc()


class ParameterHandlerImpl(ParameterHandler):
    def getParamInsertFromRequests(self):
        dataFromRequest = {
            'da_msp_id': request.json.get('product_id'),
            'da_msd_id': request.json.get('discount_id'),
            'da_start_date': request.json.get('start_date'),
            'da_expired_date': request.json.get('expired_date'),
            'da_active_status': request.json.get('active_status', 'Y')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest = {
            'da_msp_id': request.json.get('product_id'),
            'da_msd_id': request.json.get('discount_id'),
            'da_start_date': request.json.get('start_date'),
            'da_expired_date': request.json.get('expired_date'),
            'da_active_status': request.json.get('active_status')
        }
        return dataFromRequest

    def getIdFromRequest(self):
        parameterFromRequest = {
            'da_msp_id': request.json.get('product_id'),
            'da_msd_id': request.json.get('discount_id')
        }
        return parameterFromRequest

    def getOrderColumnName(self):
        orderColumnIndex = request.args.get('order[0][column]', '')
        orderColumnName = request.args.get(
            'columns[%s][name]' % orderColumnIndex, '')
        if orderColumnName == 'product_id':
            return 'da_msp_id'
        if orderColumnName == 'product_desc':
            return 'msp_desc'
        if orderColumnName == 'discount_desc':
            return 'msd_desc'
        if orderColumnName == 'discount_type':
            return 'msdt_desc'
        if orderColumnName == 'start_date':
            return 'da_start_date'
        if orderColumnName == 'expired_date':
            return 'da_expired_id'
        if orderColumnName == 'active_status':
            return 'da_active_status'
        return None


class ValidationHandlerImpl(ValidationHandler):
    def isParamSearchValid(self, dataFromRequest):
        if not dataFromRequest.get('da_msp_id'):
            return False
        if not dataFromRequest.get('da_msd_id'):
            return False
        return True

    def isParamUpdateValid(self, dataFromRequest):
        if not self.isParamInsertValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        if not self.isProductIdValid(dataFromRequest):
            return False
        if not self.isDiscountIdValid(dataFromRequest):
            return False
        if not self.isStartDateValid(dataFromRequest):
            return False
        if not self.isExpiredDateValid(dataFromRequest):
            return False
        if not self.isActiveStatusValid(dataFromRequest):
            return False
        return True

    def isParamDeleteValid(self, dataFromRequest):
        return self.isParamSearchValid(dataFromRequest)

    def isProductIdValid(self, dataFromRequest):
        if not dataFromRequest.get('da_msp_id'):
            return False
        if not self.isNumber(dataFromRequest.get('da_msp_id')):
            return False
        if int(dataFromRequest.get('da_msp_id')) < 1:
            return False
        return True

    def isDiscountIdValid(self, dataFromRequest):
        if not dataFromRequest.get('da_msd_id'):
            return False
        if not self.isNumber(dataFromRequest.get('da_msd_id')):
            return False
        if int(dataFromRequest.get('da_msd_id')) < 1:
            return False
        return True

    def isStartDateValid(self, dataFromRequest):
        if not dataFromRequest.get('da_start_date'):
            return False
        return True

    def isExpiredDateValid(self, dataFromRequest):
        if not dataFromRequest.get('da_expired_date'):
            return False
        return True

    def isActiveStatusValid(self, dataFromRequest):
        if not dataFromRequest.get('da_active_status'):
            return False
        if dataFromRequest.get('da_active_status') not in ['N', 'Y']:
            return False
        return True

    def isNumber(self, value):
        # try to parse data to numeric, if work,
        # then the data is a number.
        try:
            int(value)
        except:
            return False
        return True
