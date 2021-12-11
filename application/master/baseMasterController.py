from flask import request
from app import db
from application.utilities.response import Response


class MasterController:
    def __init__(self):
        # create instance from DataHandler, ValidationHandler and ParameterHandler. 
        # This class would be implemented by controller class.
        self.dataHandler=None
        self.validationHandler=None
        self.parameterHandler=None

    # All method bellow is a method whos being called by route function
    def getData(self):
        # try:
        data,totalRecords, totalRecordsFiltered=self.dataHandler.grabData()
        return Response.datatable(data={'datas':data,'totalRecords':totalRecords,'totalRecordsFiltered':totalRecordsFiltered})
        # except:
        #     return Response.make(status=False,msg='Eror while trying to retrieve data' )

    def insertNewData(self):
        # try:
        dataFromRequest=self.parameterHandler.getParamInsertFromRequests()
        if not self.validationHandler.isParamInsertValid(dataFromRequest):
            return Response.statusAndMsg(False,'Data is not valid, insert process has been canceled' )
        self.dataHandler.insertNewData(dataFromRequest)
        return Response.statusAndMsg(msg='Data successfully added' )
        # except:
        #     return Response.statusAndMsg(False,'Insert data failed' )

    def updateData(self):
        try:
            dataFromRequest=self.parameterHandler.getUpdateValuesFromRequests()
            if not self.validationHandler.isParamUpdateValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, update process has been canceled' )
            self.dataHandler.updateData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully updated' )
        except:
            return Response.statusAndMsg(False,'Update data failed' )

    def deleteData(self):
        try:
            dataFromRequest=self.parameterHandler.getIdFromRequest()
            if not self.validationHandler.isParamDeleteValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, delete process has been canceled' )
            self.dataHandler.deleteData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully removed' )
        except:
            return Response.statusAndMsg(False,'Data failed to removed' )

    def searchSingleData(self):
        try:
            paramFromRequest=self.parameterHandler.getIdFromRequest()
            print('is valid',self.validationHandler.isParamSearchValid(paramFromRequest))
            if not self.validationHandler.isParamSearchValid(paramFromRequest):
                return Response.make(False,'Data ID is not valid, process has been canceled' )
            singleData=self.dataHandler.grabSingleData(paramFromRequest)
            print('is data exist ',self.dataHandler.isDataExist(singleData))
            if not self.dataHandler.isDataExist(singleData):
                return Response.make(False,'Data is not found' )
            return Response.make(msg='Data Found', data=singleData)
        except:
            return Response.make(False,'Cant find data' )



class DataHandler:
    """Its abstract class. Its provide common functionality and abstract function"""
    def __init__(self):
        self.Schema=None
        self.Model=None
        self.parameterHandler=None

    def insertNewData(self,dataFromRequest):
        objectToInsert=self.Model(**dataFromRequest)
        db.session.add(objectToInsert)
        db.session.commit()

    def deleteData(self, paramFromRequest):
        objectToDelete=self.grabOne(paramFromRequest)
        db.session.delete(objectToDelete)
        db.session.commit()

    def grabSingleData(self, paramFromRequest):
        groupOfObjectResult=self.grabOne(paramFromRequest)
        return self.Schema(many=True).dump([groupOfObjectResult])

    def grabData(self):
        """Returning list of category product to be shown, total records selected
            and total records after filtered"""
        datatableConfig=self.parameterHandler.getDatatableConfiguration()
        totalRecords=self.grabTotalRecords()
        totalRecordsFiltered=None
        categoryProductData=[]
        if datatableConfig.get('searchKeyWord'):
            totalRecordsFiltered=self.grabTotalRecordsFiltered(datatableConfig)
        if bool(datatableConfig.get('searchKeyWord')) and bool(datatableConfig.get('orderBy')):
            categoryProductData= self.grabDataWithKeywordAndOrder(datatableConfig)
        elif datatableConfig.get('searchKeyWord'):
            categoryProductData= self.grabDataWithKeyword(datatableConfig)
        elif datatableConfig.get('orderBy'):
            categoryProductData= self.grabDataWithOrderby(datatableConfig)
        else:
            categoryProductData= self.grabDataDefault(datatableConfig)
        return categoryProductData,totalRecords, totalRecordsFiltered

    def grabDataDefault(self, datatableConfig):
        groupOfObjectResult=self.Model.query.offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    def grabDataWithKeywordAndOrder(self,datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=self.Model.query.filter(searchKeyWord).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    
    def grabDataWithKeyword(self,datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=self.Model.query.filter(searchKeyWord).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)
    
    def grabDataWithOrderby(self, datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=self.Model.query.order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    def isDataExist(self, queryResult):
        # first check if the array is not empty, then check if its contain empty dictionary
        if len(queryResult)<1:
            return False
        if not queryResult[0]:
            return False
        return True
    
    def updateData(self, dataFromRequest):
        pass

    def grabTotalRecords(self):
        pass
    def grabTotalRecordsFiltered(self, datatableConfig):
        pass

    def getSearchKeywordStatement(self, datatableConfig):
        pass

    def getOrderStatement(self,datatableConfig):
       pass
    def grabOne(self,paramFromRequest):
        pass
        

class ParameterHandler:
    # All method bellow is a method to process data and request
    def getDatatableConfiguration(self):
        datatableConfig={
            'searchKeyWord':request.args.get('search[value]'),
            'orderDirection':request.args.get('order[0][dir]'),
            'orderBy':self.getOrderColumnName(),
            'offset':request.args.get('start'),
            'limit':request.args.get('length')
        }
        return datatableConfig
    def getParamInsertFromRequests(self):
        pass

    def getUpdateValuesFromRequests(self):
        pass
    def geIdFromRequests(self):
        pass

    def getOrderColumnName(self):
        pass
    
        
class ValidationHandler:
    def isParamInsertValid(self, dataFromRequest):
        pass
    def isParamUpdateValid(self,dataFromRequest):
        pass

    def isParamSearchValid(self, paramFromRequest):
        pass
    def isParamDeleteValid(self, paramFromRequest):
        pass