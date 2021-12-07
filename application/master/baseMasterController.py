from flask import request
from app import db
from application.utilities.response import Response


class MasterController:
    def __init__(self):
        self.dataHandler=DataHandler()
        self.validationHandler=ValidationHandler()
        self.parameterHandler=ParameterHandler()
    # All method bellow is a method whos being called by route function
    def getData(self):
        try:
            data,totalRecords, totalRecordsFiltered=self.dataHandler.grabData()
            return Response.datatable(data={'datas':data,'totalRecords':totalRecords,'totalRecordsFiltered':totalRecordsFiltered})
        except:
            return Response.make(status=False,msg='Eror while trying to retrieve data' )

    def insertNewData(self):
        try:
            dataFromRequest=self.parameterHandler.getValuesFromRequests()
            if not self.validationHandler.isParamInsertValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, insert process has been canceled' )
            self.dataHandler.insertNewData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully added' )
        except:
            return Response.statusAndMsg(False,'Insert data failed' )

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
            dataFromRequest=self.parameterHandler.geIdFromRequests()
            if not self.validationHandler.isParamDeleteValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, delete process has been canceled' )
            self.dataHandler.deleteData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully removed' )
        except:
            return Response.statusAndMsg(False,'Data failed to removed' )

    def searchSingleData(self):
        try:
            paramFromRequest=self.parameterHandler.getIdFromRequest()
            if not self.validationHandler.isParamSearchValid(paramFromRequest):
                return Response.make(False,'Data ID is not valid, process has been canceled' )
            categoryProduct=self.dataHandler.grabSingleData(paramFromRequest)
            if not self.dataHandler.isDataExist(categoryProduct):
                return Response.make(False,'Data is not found' )
            return Response.make(msg='Data Found', data=categoryProduct)
        except:
            return Response.make(False,'Cant find data' )



class DataHandler:
    """Its abstract class. Its provide common functionality and abstract function"""
    def __init__(self):
        self.Schema=None
        self.Model=None

    def insertNewData(self,dataFromRequest):
        objectToInsert=self.Model(**dataFromRequest)
        db.session.add(objectToInsert)
        db.session.commit()
    
    def grabData(self):
        """Grab data based on parameter sended. 
            Returning list of category product to be shown, total records selected
            and total records after filtered"""
        datatableConfig=ParameterHandler().getDatatableConfiguration()
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

    def isDataExist(self, queryResult):
        if(len(queryResult)>0):
            return True
        return False
    def deleteData(self, paramFromRequest):
        pass
    
    def updateData(self, dataFromRequest):
        pass

    def grabSingleData(self, paramFromRequest):
        pass
    def grabDataDefault(self, datatableConfig):
        pass

    def grabDataWithKeywordAndOrder(self,datatableConfig):
        pass

    def grabDataWithKeyword(self,datatableConfig):
        pass

    def grabDataWithOrderby(self, datatableConfig):
        pass

    def grabTotalRecords(self):
        pass
    def grabTotalRecordsFiltered(self, datatableConfig):
        pass

    def getSearchKeywordStatement(self, datatableConfig):
        pass

    def getOrderStatement(self,datatableConfig):
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
    def getValuesFromRequests(self):
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