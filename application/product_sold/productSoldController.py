from flask import request,jsonify
from marshmallow.fields import Bool
from .productSoldModel import SoldTransactionHead, SoldTransactionDetail, SoldTransactionDetailDiscountApplied,db
from .productSoldModel import SoldTransactionHead,SoldTransactionHeadSchema
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
        try:
            dataFromRequest=ParameterHandler().getParamInsertFromRequests()
            if not ValidationHandler().isParamInsertValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, insert process has been canceled' )
            DataHandler().insertNewData(dataFromRequest)

            return Response.statusAndMsg(msg='Data successfully added' )
        except:
            return Response.statusAndMsg(False,'Insert data failed' )
    def deleteTransaction(self):
        try:
            dataFromRequest=ParameterHandler().getIdFromRequest()
            if not ValidationHandler().isParamDeleteValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data Id is not valid, delete process has been canceled' )
            DataHandler().deleteData(dataFromRequest)
            return Response.statusAndMsg(msg='Data has been deleted' )
        except:
            return Response.statusAndMsg(False,'Delete data failed' )
    def filterTransaction(self):
        return self.getData()

    def searchDetailTransaction(self):
        try:
            paramFromRequest=ParameterHandler().getIdFromRequest()
            if not ValidationHandler().isParamSearchValid(paramFromRequest):
                return Response.make(False,'Data ID is not valid, process has been canceled' )
            singleData=DataHandler().grabSingleData(paramFromRequest)
            if not DataHandler().isDataExist(singleData):
                return Response.make(False,'Data is not found' )
            return Response.make(msg='Data Found', data=singleData)
        except:
            return Response.make(False,'Cant find data' )



class DataHandler:
    def insertNewData(self,dataFromRequest):
        newHeadTransaction=SoldTransactionHead(**dataFromRequest.get("head_transaction"))
        db.session.add(newHeadTransaction)
        db.session.flush()
        self.insertDetailTransaction(dataFromRequest.get("detail_transaction"), newHeadTransaction)
        db.session.commit()
    
    def grabSingleData(self, paramFromRequest):
        groupOfObjectResult=self.grabOne(paramFromRequest)
        return SoldTransactionHeadSchema(many=True).dump([groupOfObjectResult])

    def insertDetailTransaction(self,productSold,newHeadTransaction ):
        for detailTransaction in productSold:
            discountApplied=detailTransaction.pop('discount_applied_on_transaction')
            detailTransaction.update({'td_th_id':newHeadTransaction.th_id})
            newDetailTransaction=SoldTransactionDetail(**detailTransaction)
            db.session.add(newDetailTransaction)
            db.session.flush()
            self.insertDiscountApplied(discountApplied, newDetailTransaction)

    def insertDiscountApplied(self, discountApplied, newDetailTransaction):
        for discountOnProduct in discountApplied:
            discountOnProduct.update({'tdda_td_id':newDetailTransaction.td_id})
            newDiscountAppliedDetail=SoldTransactionDetailDiscountApplied(**discountOnProduct)
            db.session.add(newDiscountAppliedDetail)
            db.session.flush()

    def deleteData(self, paramFromRequest):
        objectToDelete=self.grabOne(paramFromRequest)
        db.session.delete(objectToDelete)
        db.session.commit()

    def grabData(self):
        """Returning list of data to be shown, total records selected
            and total records after filtered"""
        datatableConfig=ParameterHandler().getDatatableConfiguration()
        isFilterExist,filterStatements=self.createFilterStatement(datatableConfig)
        totalRecords=self.grabTotalRecords()
        totalRecordsFiltered=None
        listData=[]
        if isFilterExist:
            totalRecordsFiltered=self.grabTotalRecordsFiltered(filterStatements)
        if isFilterExist and bool(datatableConfig.get('orderBy')):
            listData= self.grabDataWithKeywordAndOrder(datatableConfig,filterStatements)
        elif isFilterExist:
            listData= self.grabDataWithKeyword(datatableConfig, filterStatements)
        elif datatableConfig.get('orderBy'):
            listData= self.grabDataWithOrderby(datatableConfig)
        else:
            listData= self.grabDataDefault(datatableConfig)
        return listData,totalRecords, totalRecordsFiltered

    def createFilterStatement(self, datatableConfig):
        isFormFilterExist,formFilterStatements=self.createStatementFromFiltersForm()
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        combinedStatement=None
        if bool(datatableConfig.get('searchKeyWord')) and isFormFilterExist:
            combinedStatement=(searchKeyWord, *formFilterStatements)
        elif isFormFilterExist: 
            combinedStatement=formFilterStatements
        elif bool(datatableConfig.get('searchKeyWord')):
            combinedStatement=(searchKeyWord,)
        else:
            return False, None
        return True, combinedStatement

    def createStatementFromFiltersForm(self):
        dataFromRequest=ParameterHandler().getFilterTransactionParams()
        if not ValidationHandler().isFilterExist(dataFromRequest):
            return False, (None,)
        # saved the query statement inside list so we can append and make it more dynamic,
        #  then parse them to tuple since its the alchemy requirement
        groupOfFilterStatement=[]
        if dataFromRequest.get('td_msp_id'):
            tempStatement=(SoldTransactionDetail.td_msp_id==int(dataFromRequest.get('td_msp_id')),)
            groupOfFilterStatement.append(*tempStatement)
        if dataFromRequest.get('tdda_da_discount_id'):
            tempStatement=(SoldTransactionDetailDiscountApplied.tdda_da_discount_id==int(dataFromRequest.get('tdda_da_discount_id')),)
            groupOfFilterStatement.append(*tempStatement)
        if dataFromRequest.get('th_mse_id'):
            tempStatement=(SoldTransactionHead.th_mse_id==int(dataFromRequest.get('th_mse_id')),)
            groupOfFilterStatement.append(*tempStatement)
        if dataFromRequest.get('th_date'):
            tempStatement=(SoldTransactionHead.th_date==dataFromRequest.get('th_date'),)
            groupOfFilterStatement.append(*tempStatement)
        return True, tuple(groupOfFilterStatement)

    def getFilterStatement(self):
        dataFromRequest=ParameterHandler().getFilterTransactionParams()
        if not ValidationHandler().isFilterExist(dataFromRequest):
            return False, (None,)
        # saved the query statement inside list so we can append and make it more dynamic,
        #  then parse them to tuple since its the alchemy requirement
        groupOfFilterStatement=[]
        if dataFromRequest.get('td_msp_id'):
            tempStatement=(SoldTransactionDetail.td_msp_id==int(dataFromRequest.get('td_msp_id')),)
            groupOfFilterStatement.append(*tempStatement)
        if dataFromRequest.get('tdda_da_discount_id'):
            tempStatement=(SoldTransactionDetailDiscountApplied.tdda_da_discount_id==int(dataFromRequest.get('tdda_da_discount_id')),)
            groupOfFilterStatement.append(*tempStatement)
        if dataFromRequest.get('th_mse_id'):
            tempStatement=(SoldTransactionHead.th_mse_id==int(dataFromRequest.get('th_mse_id')),)
            groupOfFilterStatement.append(*tempStatement)
        if dataFromRequest.get('th_date'):
            tempStatement=(SoldTransactionHead.th_date==dataFromRequest.get('th_date'),)
            groupOfFilterStatement.append(*tempStatement)
        return True, tuple(groupOfFilterStatement)

    def grabDataDefault(self, datatableConfig):
        groupOfObjectResult=SoldTransactionHead.query.offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return SoldTransactionHeadSchema(many=True).dump(groupOfObjectResult)

    def grabDataWithKeywordAndOrder(self, datatableConfig,filterStatements):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=SoldTransactionHead.query.join(SoldTransactionDetail).join(SoldTransactionDetailDiscountApplied).filter(*filterStatements ).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return SoldTransactionHeadSchema(many=True).dump(groupOfObjectResult)

    
    def grabDataWithKeyword(self,datatableConfig, filterStatements):
        groupOfObjectResult=SoldTransactionHead.query.join(SoldTransactionDetail).join(SoldTransactionDetailDiscountApplied).filter(*filterStatements ).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return SoldTransactionHeadSchema(many=True).dump(groupOfObjectResult)
    
    def grabDataWithOrderby(self, datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=SoldTransactionHead.query.order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return SoldTransactionHead.Schema(many=True).dump(groupOfObjectResult)
    
    def grabTotalRecords(self):
        return db.session.query(func.count(SoldTransactionHead.th_id)).scalar()

    def grabTotalRecordsFiltered(self, filterStatements):
        return db.session.query(func.count(SoldTransactionHead.th_id.distinct())).join(SoldTransactionDetail).join(SoldTransactionDetailDiscountApplied).filter(*filterStatements ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return (SoldTransactionHead.th_id==datatableConfig.get('searchKeyWord'))

    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')
        # if columnToOrder=='msp_id': 
        #     orderStatement=self.getOrderDirectionById(orderDirection)

        return orderStatement

    def grabOne(self, paramFromRequest):
        return SoldTransactionHead.query.filter_by(th_id=paramFromRequest.get('th_id')).first()

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

    def getDiscountAppliedOnTransactionParams(self,product):
        discountAppliedOnTransaction=[]
        if not product.get('discount_applied'):
            return []
        for discountApplied in product.get('discount_applied'):
            discountOnProduct=self.getDiscountApplied(discountApplied)
            discountOnProduct.update({'tdda_da_product_id':product.get('product_id')})
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
            'td_on_sale_price':item.get('product_price'),
            'discount_applied_on_transaction':self.getDiscountAppliedOnTransactionParams(item)
            }
            detailTransactionParams.append(itemSold)
        return detailTransactionParams

    def getParamInsertFromRequests(self):
        dataFromRequests={
            'head_transaction':self.getHeadTransactionParams(),
            'detail_transaction':self.getDetailTransactionParams()
        }
        return dataFromRequests

    def getDiscountApplied(self, discount):
        discountAppliedOnProduct={
            'tdda_msdt_id':discount.get('discount_type_id'),
            'tdda_da_discount_id':discount.get('discount_id'),
            'tdda_cutt_off_nominal':discount.get('cut_off_nominal')
            }
        return discountAppliedOnProduct
    
    def getFilterTransactionParams(self):
        if not request.args:
            return {}
        dataFromRequests={
            'td_msp_id':request.args.get('product_id'),
            'tdda_da_discount_id':request.args.get('discount_id'),
            'th_mse_id':request.args.get('cashier_id'),
            'th_date':request.args.get('transaction_date')
        }
        return dataFromRequests
        
    def getIdFromRequest(self):
        parameterFromRequest={
            'th_id':request.json.get('transaction_id')
        }
        return parameterFromRequest

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
            totalPriceBeforeCuttOff =totalPriceBeforeCuttOff + (product.get('product_price',0)*product.get('quantity',0))
            totalCuttOff +=self.getCuttOffPriceItem(product.get('discount_applied'))
        totalPrice=totalPriceBeforeCuttOff - totalCuttOff
        # prevent if discount is bigger than total price
        if totalPrice<0:
            return 0
        return totalPrice


        
class ValidationHandler:
    def isParamInsertValid(self, dataFromRequest):
        if not self.validateInsertHeadTransactionParams(dataFromRequest):
            return False
        if not self.validateInsertDetailTransactionParams(dataFromRequest):
            return False
        if not self.validateDetailDiscountAppliedParams(dataFromRequest):
            return False
        return True

    def validateInsertHeadTransactionParams(self,dataFromRequest):
        if not dataFromRequest.get('head_transaction'):
            return False
        headTransactionParams=dataFromRequest.get('head_transaction')
        # set validation result as false if there is an empty value
        for key, value in headTransactionParams.items():
            if not value:
                return False
        return True

    def validateInsertDetailTransactionParams(self,dataFromRequest):
        if not dataFromRequest.get('detail_transaction'):
            return False
        detailTransactionParams=dataFromRequest.get('detail_transaction')
        # set validation result as false if there is an empty value
        for productSold in detailTransactionParams:
            for key, value in productSold.items():
                if key=='discount_applied_on_transaction':
                    continue
                if not value:
                    return False
        return True

    def validateDetailDiscountAppliedParams(self,dataFromRequest):
        for productSold in  dataFromRequest.get('detail_transaction'):
            if not dataFromRequest.get('discount_applied_on_transaction'):
                return True
            for discountApplied in productSold.get('discount_applied_on_transaction'):
                if not self.isFalsyValueFound(discountApplied):
                    return False
        return True

    def isFalsyValueFound(self, listOfDictData):
        for dictData in listOfDictData:
            for key, value in dictData.items():
                if not value:
                    return False
        return True
    def isIdValid(self,dataFromRequest):
        if not dataFromRequest.get('th_id'):
            return False
        if not self.isNumber(dataFromRequest.get('th_id')):
            return False
        return True
    def isParamDeleteValid(self,dataFromRequest):
        return self.isIdValid(dataFromRequest)
    def isParamSearchValid(self,dataFromRequest):
        return self.isIdValid(dataFromRequest)
    
    def isFilterExist(self,dataFromRequest):
        # check at dictionary, if there is an item, return true. Return false instead if all key is empty
        falsyValueGroup=[]
        for key, value in dataFromRequest.items():
            if value:
                falsyValueGroup.append(True)
        if falsyValueGroup:
            return True
        return False
    
    def isNumber(self,value):
        # try to parse data to numeric, if work, 
        # then the data is a number.
        try:
            int(value)
        except:
            return False
        return True
