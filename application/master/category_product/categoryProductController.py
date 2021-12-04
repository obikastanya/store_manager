from flask import request
from .categoryProductModel import db,CategoryProductSchema, CategoryProduct
from sqlalchemy import func
from application.utilities.response import Response

class CategoryProductController:
    # All method bellow is a method whos being called by route function
    def getData(self):
        try:
            categoryProductData,totalRecords, totalRecordsFiltered=DataHandler().grabData()
            return Response.datatable(data={'datas':categoryProductData,'totalRecords':totalRecords,'totalRecordsFiltered':totalRecordsFiltered})
        except:
            return Response.make(status=False,msg='Eror while trying to retrieve data' )

    def insertNewData(self):
        try:
            dataFromRequest=ParameterHandler().getCategoryFromRequests()
            if not ValidationHandler().isParamInsertValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, insert process has been canceled' )
            DataHandler().insertNewData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully added' )
        except:
            return Response.statusAndMsg(False,'Insert data failed' )

    def updateData(self):
        try:
            dataFromRequest=ParameterHandler().getUpdatedCategoryFromRequests()
            if not ValidationHandler().isParamUpdateValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, update process has been canceled' )
            DataHandler().updateData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully updated' )
        except:
            return Response.statusAndMsg(False,'Update data failed' )

    def deleteData(self):
        try:
            dataFromRequest=ParameterHandler().getDeleteIdCategoryFromRequests()
            if not ValidationHandler().isParamDeleteValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, delete process has been canceled' )
            DataHandler().deleteData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully removed' )
        except:
            return Response.statusAndMsg(False,'Data failed to removed' )

    def searchSingleData(self):
        try:

            paramFromRequest=ParameterHandler().getSearchParameterFromRequest()
            if not ValidationHandler().isParamSearchValid(paramFromRequest):
                return Response.make(False,'Category ID is not valid, process has been canceled' )
            categoryProduct=DataHandler().grabSingleData(paramFromRequest)
            if not DataHandler().isDataExist(categoryProduct):
                return Response.make(False,'Category product is not found' )
            return Response.make(msg='Data Found', data=categoryProduct)
        except:
            return Response.make(False,'Cant find data' )
    

class ParameterHandler:
    # All method bellow is a method to process data and request
    def getCategoryFromRequests(self):
        dataFromRequest={
            'msc_desc':request.json.get('category'),
            'msc_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdatedCategoryFromRequests(self):
        dataFromRequest={
            'msc_desc':request.json.get('category'),
            'msc_active_status':request.json.get('active_status'),
            'msc_id':request.json.get('category_id')
        }
        return dataFromRequest
    def getSearchParameterFromRequest(self):
        parameterFromRequest={
            'msc_id':request.json.get('category_id')
        }
        return parameterFromRequest
    def getDeleteIdCategoryFromRequests(self):
        return self.getSearchParameterFromRequest()

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='category_id':
            return 'msc_id'
        if orderColumnName=='category':
            return 'msc_desc'
        if orderColumnName=='active_status':
            return 'msc_active_status'
        return None
    
    def getDatatableConfiguration(self):
        datatableConfig={
            'searchKeyWord':request.args.get('search[value]'),
            'orderDirection':request.args.get('order[0][dir]'),
            'orderBy':self.getOrderColumnName(),
            'offset':request.args.get('start'),
            'limit':request.args.get('length')
        }
        return datatableConfig

    

class DataHandler:
    def insertNewData(self,dataFromRequest):
        objectToInsert=CategoryProduct(**dataFromRequest)
        db.session.add(objectToInsert)
        db.session.commit()
        
    def deleteData(self, paramFromRequest):
        objectToDelete=CategoryProduct.query.filter_by(msc_id=paramFromRequest.get('msc_id'))
        db.session.delete(objectToDelete[0])
        db.session.commit()
    
    def updateData(self, dataFromRequest):
        categoryProduct=CategoryProduct.query.filter_by(msc_id=dataFromRequest.get('msc_id')).first()
        categoryProduct.msc_desc=dataFromRequest.get('msc_desc')
        categoryProduct.msc_active_status=dataFromRequest.get('msc_active_status')
        db.session.commit()

    def grabSingleData(self, paramFromRequest):
        groupOfObjectResult=CategoryProduct.query.filter_by(msc_id=paramFromRequest.get('msc_id'))
        return CategoryProductSchema(many=True).dump(groupOfObjectResult)

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

    def grabDataDefault(self, datatableConfig):
        groupOfObjectResult=CategoryProduct.query.offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return CategoryProductSchema(many=True).dump(groupOfObjectResult)

    def grabDataWithKeywordAndOrder(self,datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=CategoryProduct.query.filter(searchKeyWord).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return CategoryProductSchema(many=True).dump(groupOfObjectResult)

    def grabDataWithKeyword(self,datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=CategoryProduct.query.filter(searchKeyWord).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return CategoryProductSchema(many=True).dump(groupOfObjectResult)

    def grabDataWithOrderby(self, datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=CategoryProduct.query.order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return CategoryProductSchema(many=True).dump(groupOfObjectResult)

    def grabTotalRecords(self):
        return db.session.query(func.count(CategoryProduct.msc_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(CategoryProduct.msc_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return CategoryProduct.msc_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
        
    def isDataExist(self, dataCategoryProduct):
        if(len(dataCategoryProduct)>0):
            return True
        return False

    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='msc_id': 
            if orderDirection=='asc':
                orderStatement=CategoryProduct.msc_id.asc()
            if orderDirection=='desc':
                orderStatement=CategoryProduct.msc_id.desc()

        if columnToOrder=='msc_desc':
            if orderDirection=='asc':
                orderStatement=CategoryProduct.msc_desc.asc()
            if orderDirection=='desc':
                orderStatement=CategoryProduct.msc_desc.desc()

        if columnToOrder=='msc_active_status':
            if orderDirection=='asc':
                orderStatement=CategoryProduct.msc_active_status.asc()
            if orderDirection=='desc':
                orderStatement=CategoryProduct.msc_active_status.desc()

        return orderStatement
        
        
class ValidationHandler:
    def isCategoryValid(self,dataFromRequest):
        if not dataFromRequest.get('msc_desc'):
            return False
        if len(dataFromRequest.get('msc_desc'))<3:
            return False
        if len(dataFromRequest.get('msc_desc'))>200:
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        return self.isCategoryValid(dataFromRequest)

    def isParamUpdateValid(self,dataFromRequest):
        if not dataFromRequest.get('msc_id'):
            return False
        if not dataFromRequest.get('msc_active_status'):
            return False
        if not  self.isCategoryValid(dataFromRequest):
            return False
        return True

    def isParamSearchValid(self, paramFromRequest):
        if not paramFromRequest.get('msc_id'):
            return False
        return True
    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)