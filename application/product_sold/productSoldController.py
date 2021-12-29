from itertools import product
from flask import request,jsonify
from marshmallow.fields import Int
from werkzeug.utils import send_file
from .productSoldModel import SoldTransactionHead,SoldTransactionDetail, SoldTransactionDetailDiscountApplied,db
from .productSoldModel import SoldTransactionHeadSchema,SoldTransactionDetailSchema, SoldTransactionDetailDiscountAppliedSchema
from application.utilities.response import Response
from sqlalchemy import func

class ProductSoldController:
    def defaultFalse(self):
        return {'status':False,'msg':'default false msg'}
        
    def getData(self):
        try:
            data,totalRecords, totalRecordsFiltered=DataHandler().grabData()
            resp= Response.datatable(data={'datas':data,'totalRecords':totalRecords,'totalRecordsFiltered':totalRecordsFiltered})
            return resp
        except:
            return Response.make(status=False,msg='Eror while trying to retrieve data' )

    def insertNewTransaction(self):
        # try:
        dataFromRequest=ParameterHandler().getParamInsertFromRequests()
        print(dataFromRequest)
        return self.defaultFalse()
        # if not ValidationHandler().isParamInsertValid(dataFromRequest):
        #     return Response.statusAndMsg(False,'Data is not valid, insert process has been canceled' )
        # DataHandler().insertNewData(dataFromRequest)
        # return Response.statusAndMsg(msg='Data successfully added' )
        # except:
        #     return Response.statusAndMsg(False,'Insert data failed' )
    def deleteTransaction(self):
        return self.defaultFalse()
    def filterTransaction(self):
        return self.defaultFalse()
    def searchDetailTransaction(self):
        return self.defaultFalse()

class DataHandler:
    def insertNewData(self,dataFromRequest):
        objectToInsert=self.Model(**dataFromRequest)
        db.session.add(objectToInsert)
        db.session.commit()

    def grabData(self):
        """Returning list of data to be shown, total records selected
            and total records after filtered"""
        datatableConfig=ParameterHandler().getDatatableConfiguration()
        totalRecords=self.grabTotalRecords()
        totalRecordsFiltered=None
        listData=[]
        if datatableConfig.get('searchKeyWord'):
            totalRecordsFiltered=self.grabTotalRecordsFiltered(datatableConfig)
        if bool(datatableConfig.get('searchKeyWord')) and bool(datatableConfig.get('orderBy')):
            listData= self.grabDataWithKeywordAndOrder(datatableConfig)
        elif datatableConfig.get('searchKeyWord'):
            listData= self.grabDataWithKeyword(datatableConfig)
        elif datatableConfig.get('orderBy'):
            listData= self.grabDataWithOrderby(datatableConfig)
        else:
            listData= self.grabDataDefault(datatableConfig)
        return listData,totalRecords, totalRecordsFiltered

    def grabDataDefault(self, datatableConfig):
        groupOfObjectResult=SoldTransactionHead.query.offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return SoldTransactionHeadSchema(many=True).dump(groupOfObjectResult)

    def grabDataWithKeywordAndOrder(self,datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=SoldTransactionHead.query.filter(searchKeyWord).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return SoldTransactionHeadSchema(many=True).dump(groupOfObjectResult)

    
    def grabDataWithKeyword(self,datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=SoldTransactionHead.query.filter(searchKeyWord).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return SoldTransactionHeadSchema(many=True).dump(groupOfObjectResult)
    
    def grabDataWithOrderby(self, datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=SoldTransactionHead.query.order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return SoldTransactionHead.Schema(many=True).dump(groupOfObjectResult)
    
    def grabTotalRecords(self):
        return db.session.query(func.count(SoldTransactionHead.th_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(SoldTransactionHead.th_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return (SoldTransactionHead.th_id==datatableConfig.get('searchKeyWord'))

    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')
        # if columnToOrder=='msp_id': 
        #     orderStatement=self.getOrderDirectionById(orderDirection)

        return orderStatement

    def grabOne(self,paramFromRequest):
        pass

    def isDataExist(self, queryResult):
        # first check if the array is not empty, then check if its contain empty dictionary
        if len(queryResult)<1:
            return False
        if not queryResult[0]:
            return False
        return True
    

class ParameterHandler:
    def getDatatableConfiguration(self):
        datatableConfig={
            'searchKeyWord':request.args.get('search[value]'),
            'orderDirection':request.args.get('order[0][dir]'),
            'orderBy':self.getOrderColumnName(),
            'offset':request.args.get('start'),
            'limit':request.args.get('length')
        }
        return datatableConfig

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='product_id':
            return 'msp_id'
        return None


    def getHeadTransactionParams(self):
        headTransactionParam={
            'th_mspm_id':request.json.get('payment_method'),
            'th_mse_id':request.json.get('cashier_id'),
            'th_paid':request.json.get('paid'),
            'th_date':request.json.get('transaction_date'),
            'th_total_price':self.countTotalPrice(),
            'th_change':self.countChange(),
            'th_tax':self.countTax()
        }
        return headTransactionParam

    def getDiscountAppliedOnTransactionParams(self):
        discountAppliedOnTransaction=[]
        if not request.json.get('product_sold'):
           return []
        for product in request.json.get('product_sold'):
            if not product.get('discount_applied'):
                continue
            for discountApplied in product.get('discount_applied'):
                discountOnProduct=self.getDiscountApplied(discountApplied)
                discountAppliedOnTransaction.append(discountOnProduct)
        return discountAppliedOnTransaction

    def getDetailTransactionParams(self):
        if not request.json.get('product_sold'):
           return []
        productSold= request.json.get('product_sold')
        detailTransactionParams=[]
        for item in productSold:
            itemSold={
            'td_msp_id':item.get('product_id'),
            'td_quantity':item.get('quantity'),
            'td_on_sale_price':item.get('product_price')
            }
            detailTransactionParams.append(itemSold)
        return detailTransactionParams

    def getParamInsertFromRequests(self):
        dataFromRequests={
            'head_transaction':self.getHeadTransactionParams(),
            'detail_transaction':self.getDetailTransactionParams(),
            'discount_applied_on_transaction':self.getDiscountAppliedOnTransactionParams()
        }
        return dataFromRequests

    def getDiscountApplied(self, discount):
        discountAppliedOnProduct={
            'tdda_msdt_id':discount.get('discount_id'),
            'tdda_da_product_id':discount.get('discount_type_id'),
            'tdda_da_discount_id':discount.get('cut_off_nominal')
            }
        return discountAppliedOnProduct

    def countChange(self):
        return  request.json.get('paid',0)-(self.countTotalPrice()+self.countTax())

    def countTax(self):
        return self.countTotalPrice()*0.1

    def getCuttOffPriceItem(self,discountAppliedOnItem):
        if not discountAppliedOnItem:
            return 0
        totalDiscountOnItem=0
        for discount in discountAppliedOnItem:
            totalDiscountOnItem+=discount.get('cutt_off_nominal',0)
        return totalDiscountOnItem

    def countTotalPrice(self):
        productSold=request.json.get('product_sold')
        totalPriceBeforeCuttOff=0
        totalCuttOff=0
        for product in productSold:
            totalPriceBeforeCuttOff =totalPriceBeforeCuttOff + product.get('product_price',0)
            totalCuttOff +=self.getCuttOffPriceItem(product.get('discount_applied'))
        return totalPriceBeforeCuttOff - totalCuttOff


        
class ValidationHandler:
    def isParamInsertValid(self, dataFromRequest):
        return True