from flask import request,jsonify
from .productPurchasedModel import PurchasedTransactionHead, PurchasedTransactionDetail,db
from .productPurchasedModel import PurchasedTransactionHeadSchema,PurchasedTransactionDetailSchema
from ..master.supplier.supplierModel import Supplier
from ..master.employee.employeeModel import Employee
from ..master.payment_method.paymentMethodModel import PaymentMethod
from application.utilities.response import Response
from sqlalchemy import func

# from ..product_sold.productSoldModel import SoldTransactionHead, SoldTransactionDetail, SoldTransactionDetailDiscountApplied
# from ..product_sold.productSoldModel import SoldTransactionHead,SoldTransactionHeadSchema

class ProductPurchasedController:
    def defaultFalse(self):
        return {'status':False,'msg':'default false msg'}
        
    def getData(self):
        # return self.defaultFalse()
        # try:
        data,totalRecords, totalRecordsFiltered=DataHandler().grabData()
        resp= Response.datatable(data={'datas':data,'totalRecords':totalRecords,'totalRecordsFiltered':totalRecordsFiltered})
        return resp
        # except:
        #     return Response.make(status=False,msg='Eror while trying to retrieve data' )

    def insertNewTransaction(self):
        # return self.defaultFalse()
        # try:
        dataFromRequest=ParameterHandler().getParamInsertFromRequests()
        if not ValidationHandler().isParamInsertValid(dataFromRequest):
            return Response.statusAndMsg(False,'Data is not valid, insert process has been canceled' )
        DataHandler().insertNewData(dataFromRequest)

        return Response.statusAndMsg(msg='Data successfully added' )
        # except:
        #     return Response.statusAndMsg(False,'Insert data failed' )
    def deleteTransaction(self):
        return self.defaultFalse()
        try:
            dataFromRequest=ParameterHandler().getIdFromRequest()
            if not ValidationHandler().isParamDeleteValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data Id is not valid, delete process has been canceled' )
            DataHandler().deleteData(dataFromRequest)
            return Response.statusAndMsg(msg='Data has been deleted' )
        except:
            return Response.statusAndMsg(False,'Delete data failed' )
    def filterTransaction(self):
        return self.defaultFalse()
        return self.getData()

    def searchDetailTransaction(self):
        return self.defaultFalse()
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
        newHeadTransaction=PurchasedTransactionHead(**dataFromRequest.get("head_transaction"))
        db.session.add(newHeadTransaction)
        db.session.flush()
        self.insertDetailTransaction(dataFromRequest.get("detail_transaction"), newHeadTransaction)
        db.session.commit()

    def insertDetailTransaction(self,productPurchased,newHeadTransaction ):
        for detailTransaction in productPurchased:
            detailTransaction.update({'tpd_tp_id':newHeadTransaction.tp_id})
            newDetailTransaction=PurchasedTransactionDetail(**detailTransaction)
            db.session.add(newDetailTransaction)
            db.session.flush()
    
    # def grabSingleData(self, paramFromRequest):
    #     groupOfObjectResult=self.grabOne(paramFromRequest)
    #     return SoldTransactionHeadSchema(many=True).dump([groupOfObjectResult])

    # def deleteData(self, paramFromRequest):
    #     objectToDelete=self.grabOne(paramFromRequest)
    #     db.session.delete(objectToDelete)
    #     db.session.commit()
    
    def grabOne(self, paramFromRequest):
        return PurchasedTransactionHead.query.filter_by(th_id=paramFromRequest.get('tp_id')).first()

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
        # then parse them to tuple since its the alchemy requirement
        groupOfFilterStatement=[]
        if dataFromRequest.get('tp_mssp_id'):
            tempStatement=(PurchasedTransactionHead.tp_mssp_id==int(dataFromRequest.get('tp_mssp_id')),)
            groupOfFilterStatement.append(*tempStatement)
        if dataFromRequest.get('tp_date'):
            tempStatement=(PurchasedTransactionHead.tp_date==dataFromRequest.get('tp_date'),)
            groupOfFilterStatement.append(*tempStatement)
        if dataFromRequest.get('tpd_msp_id'):
            tempStatement=(PurchasedTransactionDetail.tpd_msp_id==int(dataFromRequest.get('tpd_msp_id')),)
            groupOfFilterStatement.append(*tempStatement)
        return True, tuple(groupOfFilterStatement)

    def grabDataDefault(self, datatableConfig):
        groupOfObjectResult=self.getQueryJoined().offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return PurchasedTransactionHeadSchema(many=True).dump(groupOfObjectResult)

    def grabDataWithKeywordAndOrder(self, datatableConfig,filterStatements):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=self.getQueryJoined().filter(*filterStatements ).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return PurchasedTransactionHeadSchema(many=True).dump(groupOfObjectResult)

    
    def grabDataWithKeyword(self,datatableConfig, filterStatements):
        groupOfObjectResult=self.getQueryJoined().filter(*filterStatements ).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return PurchasedTransactionHeadSchema(many=True).dump(groupOfObjectResult)
    
    def grabDataWithOrderby(self, datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=self.getQueryJoined().order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return PurchasedTransactionHeadSchema(many=True).dump(groupOfObjectResult)
    
    def grabTotalRecords(self):
        return db.session.query(func.count(PurchasedTransactionHead.tp_id)).scalar()

    def grabTotalRecordsFiltered(self, filterStatements):
        return db.session.query(func.count(PurchasedTransactionHead.tp_id.distinct())).join(PurchasedTransactionDetail).filter(*filterStatements ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return (PurchasedTransactionHead.tp_id==datatableConfig.get('searchKeyWord'))

    def getQueryJoined(self):
        return PurchasedTransactionHead.query.join(Supplier).join(PaymentMethod).join(PurchasedTransactionDetail)

    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')
        if columnToOrder=='th_id':
            orderStatement=self.getOrderByTransactionHeadId(orderDirection)
        if columnToOrder=='th_date':
            orderStatement=self.getOrderByTransactionDate(orderDirection)
        if columnToOrder=='th_mse_id':
            orderStatement=self.getOrderByCashier(orderDirection)
        if columnToOrder=='th_mspm_id':
            orderStatement=self.getOrderByPaymentMethod(orderDirection)
        if columnToOrder=='th_total_price':
            orderStatement=self.getOrderByTotalPrice(orderDirection)
        if columnToOrder=='th_tax':
            orderStatement=self.getOrderByTax(orderDirection)
        if columnToOrder=='th_paid':
            orderStatement=self.getOrderByPaid(orderDirection)
        if columnToOrder=='th_change':
            orderStatement=self.getOrderByChange(orderDirection)
        return orderStatement

    def getOrderByTransactionHeadId(self,orderDirection):
        if orderDirection=='desc':
            return SoldTransactionHead.th_id.desc()
        return SoldTransactionHead.th_id.asc()

    def getOrderByTransactionDate(self, orderDirection):
        if orderDirection=='desc':
            return SoldTransactionHead.th_date.desc()
        return SoldTransactionHead.th_date.asc()

    def getOrderByCashier(self, orderDirection):
        if orderDirection=='desc':
            return Employee.mse_name.desc()
        return Employee.mse_name.asc()

    def getOrderByPaymentMethod(self, orderDirection):
        if orderDirection=='desc':
            return PaymentMethod.mspm_desc.desc()
        return PaymentMethod.mspm_desc.asc()

    def getOrderByTotalPrice(self,orderDirection):
        if orderDirection=='desc':
            return SoldTransactionHead.th_total_price.desc()
        return SoldTransactionHead.th_total_price.asc()

    def getOrderByTax(self, orderDirection):
        if orderDirection=='desc':
            return SoldTransactionHead.th_tax.desc()
        return SoldTransactionHead.th_tax.asc()

    def getOrderByPaid(self, orderDirection):
        if orderDirection=='desc':
            return SoldTransactionHead.th_paid.desc()
        return SoldTransactionHead.th_paid.asc()

    def getOrderByChange(self,orderDirection):
        if orderDirection=='desc':
            return SoldTransactionHead.th_change.desc()
        return SoldTransactionHead.th_change.asc()

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
        if orderColumnName=='transaction_id':
            return 'th_id'
        if orderColumnName=='transaction_date':
            return 'th_date'
        if orderColumnName=='employee_transaction':
            return 'th_mse_id'
        if orderColumnName=='payment_method':
            return 'th_mspm_id'
        if orderColumnName=='total_price':
            return 'th_total_price'
        if orderColumnName=='tax':
            return 'th_tax'
        if orderColumnName=='paid':
            return 'th_paid'
        if orderColumnName=='change':
            return 'th_change'
        return None


    def getHeadTransactionParams(self):
        headTransactionParam={
            'tp_mssp_id':request.json.get('supplier_id'),
            'tp_mspm_id':request.json.get('payment_method'),
            'tp_nominal':request.json.get('nominal'),
            'tp_date':request.json.get('transaction_date')
        }
        return headTransactionParam

    def getDetailTransactionParams(self):
        if not request.json.get('product_purchased'):
           return []
        productSold= request.json.get('product_purchased')
        detailTransactionParams=[]
        for item in productSold:
            itemSold={
            'tpd_msp_id':item.get('product_id'),
            'tpd_quantity':item.get('quantity'),
            'tpd_msp_price':item.get('product_price')
            }
            detailTransactionParams.append(itemSold)
        return detailTransactionParams

    def getParamInsertFromRequests(self):
        dataFromRequests={
            'head_transaction':self.getHeadTransactionParams(),
            'detail_transaction':self.getDetailTransactionParams()
        }
        return dataFromRequests

    def getFilterTransactionParams(self):
        if not request.args:
            return {}
        dataFromRequests={
            'tp_mssp_id':request.args.get('supplier_id'),
            'tpd_msp_id':request.args.get('product_id'),
            'tp_date':request.args.get('transaction_date')
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
            if value in [0,0.0]:
                continue
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
                if value in [0,0.0]:
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
