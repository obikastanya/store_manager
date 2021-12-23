from flask import request
from marshmallow.fields import Constant
from sqlalchemy import func
from sqlalchemy.sql.expression import select
from application.master.product.productModel import Product
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler
from ..stock.stockModel import db, Stock, StockSchema
from ..product.productModel import Product


class StockController(MasterController):
    def __init__(self):
        super().__init__()
        self.dataHandler=DataHandlerImpl()
        self.validationHandler=ValidationHandlerImpl()
        self.parameterHandler=ParameterHandlerImpl()

class DataHandlerImpl(DataHandler):
    def __init__(self):
        super().__init__()
        self.Model=Stock
        self.Schema=StockSchema
        self.parameterHandler=ParameterHandlerImpl()


    def updateData(self, dataFromRequest):
        stock=self.grabOne(dataFromRequest)
        stock.mss_warehouse_stock=dataFromRequest.get('mss_warehouse_stock')
        stock.mss_store_stock=dataFromRequest.get('mss_store_stock')
        db.session.commit()

    def grabDataWithKeywordAndOrder(self,datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=db.session.query(self.Model).join(Product).filter(searchKeyWord).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    
    def grabDataWithKeyword(self,datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=db.session.query(self.Model).join(Product).filter(searchKeyWord).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)
    
    def grabDataWithOrderby(self, datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=db.session.query(self.Model).join(Product).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    def grabOne(self, paramFromRequest):
        return self.Model.query.filter_by(mss_id=paramFromRequest.get('mss_id')).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.mss_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.mss_id)).join(Product).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return Product.msp_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')
        if columnToOrder=='mss_id': 
            orderStatement=self.getOrderDirectionById(orderDirection)
        if columnToOrder=='msp_desc':
            orderStatement=self.getOrderDirectionProductDesc( orderDirection)
        if columnToOrder=='msp_id':
            orderStatement=self.getOrderDirectionProductId( orderDirection)
        elif columnToOrder=='mss_warehouse_stock':
            orderStatement=self.getOrderByWarehouseStock(orderDirection)
        elif columnToOrder=='mss_store_stock':
            orderStatement=self.getOrderByStoreStock(orderDirection)
        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mss_id.desc()
        return self.Model.mss_id.asc()

    def getOrderDirectionProductDesc(self, orderDirection):
        if orderDirection=='desc':
            return Product.msp_desc.desc()
        return Product.msp_desc.asc()

    def getOrderDirectionProductId(self, orderDirection):
        if orderDirection=='desc':
            return Product.msp_id.desc()
        return Product.msp_id.asc()

    def getOrderByWarehouseStock(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.mss_warehouse_stock.desc()
        return self.Model.mss_warehouse_stock.asc()

    def getOrderByStoreStock(self,orderDirection):
        if orderDirection=='desc':
            return self.Model.mss_store_stock.desc()
        return self.Model.mss_store_stock.asc()

class ParameterHandlerImpl(ParameterHandler):
    def getParamInsertFromRequests(self):
        dataFromRequest={
            'mss_warehouse_stock':request.json.get('warehouse_stock'),
            'mss_store_stock':request.json.get('store_stock'),
            'mss_msp_id':request.json.get('product_id')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest={
            'mss_store_stock':request.json.get('store_stock'),
            'mss_warehouse_stock':request.json.get('warehouse_stock'),
            'mss_msp_id':request.json.get('product_id'),
            'mss_id':request.json.get('stock_id')
        }
        return dataFromRequest

    def getIdFromRequest(self):
        parameterFromRequest={
            'mss_id':request.json.get('stock_id')
        }
        return parameterFromRequest

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='stock_id':
            return 'mss_id'
        if orderColumnName=='product_desc':
            return 'msp_desc'
        if orderColumnName=='product_id':
            return 'msp_id'
        if orderColumnName=='warehouse_stock':
            return 'mss_warehouse_stock'
        if orderColumnName=='store_stock':
            return 'mss_store_stock'
        return None

class ValidationHandlerImpl(ValidationHandler):
    def isParamSearchValid(self, paramFromRequest):
            if not paramFromRequest.get('mss_id'):
                return False
            return True

    def isParamUpdateValid(self,dataFromRequest):
        if not dataFromRequest.get('mss_id'):
            return False
        if not self.isProductIdValid(dataFromRequest):
            return False
        if not self.isWarehouseStockValid(dataFromRequest):
            return False
        if not self.isStoreStockValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        if not self.isProductIdValid(dataFromRequest):
            return False
        if not self.isWarehouseStockValid(dataFromRequest):
            return False
        if not self.isStoreStockValid(dataFromRequest):
            return False
        return True

    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)

    def isWarehouseStockValid(self,dataFromRequest):
        if not dataFromRequest.get('mss_warehouse_stock'):
            return False
        if not self.isNumber(dataFromRequest.get('mss_warehouse_stock')):
            return False
        if int(dataFromRequest.get('mss_warehouse_stock'))<0:
            return False
        if len(str(dataFromRequest.get('mss_warehouse_stock')))>8:
            return False
        return True

    def isStoreStockValid(self,dataFromRequest):
        if not dataFromRequest.get('mss_store_stock'):
            return False
        if not self.isNumber(dataFromRequest.get('mss_store_stock')):
            return False
        if int(dataFromRequest.get('mss_store_stock'))<0:
            return False
        if len(str(dataFromRequest.get('mss_store_stock')))>8:
            return False
        return True
    def isProductIdValid(self,dataFromRequest):
        if not dataFromRequest.get('mss_msp_id'):
            return False
        if not self.isNumber(dataFromRequest.get('mss_msp_id')):
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
