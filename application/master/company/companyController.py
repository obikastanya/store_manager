from flask import request
from .companyModel import db,Company, CompanySchema
from application.utilities.response import Response
from sqlalchemy import func

class CompanyController:
    def insertNewData(self):
        try:
            dataFromRequest=ParameterHandler().getCompanyFromRequests()
            if not ValidationHandler().isParamInsertValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, insert process has been canceled' )
            DataHandler().insertNewData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully added' )
        except:
            return Response.statusAndMsg(False,'Insert data failed' )

    def getData(self):
        try:
            companyData,totalRecords, totalRecordsFiltered=DataHandler().grabData()
            return Response.datatable(data={'datas':companyData,'totalRecords':totalRecords,'totalRecordsFiltered':totalRecordsFiltered})
        except:
            return Response.make(status=False,msg='Eror while trying to retrieve data' )

    def searchSingleData(self):
        try:
            paramFromRequest=ParameterHandler().getSearchParameterFromRequest()
            if not ValidationHandler().isParamSearchValid(paramFromRequest):
                return Response.make(False,'Company ID is not valid, process has been canceled' )
            company=DataHandler().grabSingleData(paramFromRequest)
            if not DataHandler().isDataExist(company):
                return Response.make(False,'Company is not found' )
            return Response.make(msg='Data Found', data=company)
        except:
            return Response.make(False,'Cant find data' )

    def updateData(self):
        try:
            dataFromRequest=ParameterHandler().getUpdatedCompanyFromRequests()
            if not ValidationHandler().isParamUpdateValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, update process has been canceled' )
            DataHandler().updateData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully updated' )
        except:
            return Response.statusAndMsg(False,'Update data failed' )
    def deleteData(self):
        try:
            dataFromRequest=ParameterHandler().getDeleteIdCompanyFromRequests()
            if not ValidationHandler().isParamDeleteValid(dataFromRequest):
                return Response.statusAndMsg(False,'Data is not valid, delete process has been canceled' )
            DataHandler().deleteData(dataFromRequest)
            return Response.statusAndMsg(msg='Data successfully removed' )
        except:
            return Response.statusAndMsg(False,'Data failed to removed' )
    

class DataHandler:
    def insertNewData(self,dataFromRequest):
        objectToInsert=Company(**dataFromRequest)
        db.session.add(objectToInsert)
        db.session.commit()

    def deleteData(self, paramFromRequest):
        objectToDelete=Company.query.filter_by(mscp_id=paramFromRequest.get('mscp_id'))
        db.session.delete(objectToDelete[0])
        db.session.commit()

    def updateData(self, dataFromRequest):
        categoryProduct=Company.query.filter_by(mscp_id=dataFromRequest.get('mscp_id')).first()
        categoryProduct.mscp_desc=dataFromRequest.get('mscp_desc')
        categoryProduct.mscp_active_status=dataFromRequest.get('mscp_active_status')
        db.session.commit()
        
    def grabSingleData(self, paramFromRequest):
        groupOfObjectResult=Company.query.filter_by(mscp_id=paramFromRequest.get('mscp_id'))
        return CompanySchema(many=True).dump(groupOfObjectResult)

    def grabData(self):
        """Grab data based on parameter sended. 
            Returning list of category product to be shown, total records selected
            and total records after filtered"""
        datatableConfig=ParameterHandler().getDatatableConfiguration()
        totalRecords=self.grabTotalRecords()
        totalRecordsFiltered=None
        companyData=[]
        if datatableConfig.get('searchKeyWord'):
            totalRecordsFiltered=self.grabTotalRecordsFiltered(datatableConfig)
        if bool(datatableConfig.get('searchKeyWord')) and bool(datatableConfig.get('orderBy')):
            companyData= self.grabDataWithKeywordAndOrder(datatableConfig)
        elif datatableConfig.get('searchKeyWord'):
            companyData= self.grabDataWithKeyword(datatableConfig)
        elif datatableConfig.get('orderBy'):
            companyData= self.grabDataWithOrderby(datatableConfig)
        else:
            companyData= self.grabDataDefault(datatableConfig)
        return companyData,totalRecords, totalRecordsFiltered
        
    def grabDataDefault(self, datatableConfig):
        groupOfObjectResult=Company.query.offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return CompanySchema(many=True).dump(groupOfObjectResult)

    def grabDataWithKeywordAndOrder(self,datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=Company.query.filter(searchKeyWord).order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return CompanySchema(many=True).dump(groupOfObjectResult)

    def grabDataWithKeyword(self,datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        groupOfObjectResult=Company.query.filter(searchKeyWord).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return CompanySchema(many=True).dump(groupOfObjectResult)

    def grabDataWithOrderby(self, datatableConfig):
        orderStatement=self.getOrderStatement(datatableConfig)
        groupOfObjectResult=Company.query.order_by(orderStatement).offset(datatableConfig.get('offset')).limit(datatableConfig.get('limit')).all()
        return CompanySchema(many=True).dump(groupOfObjectResult)

    def grabTotalRecords(self):
        return db.session.query(func.count(Company.mscp_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(Company.mscp_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return Company.mscp_desc.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def isDataExist(self, dataCompany):
        if(len(dataCompany)>0):
            return True
        return False
        
class ParameterHandler:
    def getCompanyFromRequests(self):
        dataFromRequest={
            'mscp_desc':request.json.get('company'),
            'mscp_active_status':request.json.get('active_status','Y')
        }
        return dataFromRequest

    def getUpdatedCompanyFromRequests(self):
        dataFromRequest={
            'mscp_desc':request.json.get('company'),
            'mscp_active_status':request.json.get('active_status'),
            'mscp_id':request.json.get('company_id')
        }
        return dataFromRequest

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='company_id':
            return 'mscp_id'
        if orderColumnName=='company':
            return 'mscp_desc'
        if orderColumnName=='active_status':
            return 'mscp_active_status'
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
    def getSearchParameterFromRequest(self):
        parameterFromRequest={
            'mscp_id':request.json.get('company_id')
        }
        return parameterFromRequest
    def getDeleteIdCompanyFromRequests(self):
        return self.getSearchParameterFromRequest()


class ValidationHandler:
    def isCompanyValid(self,dataFromRequest):
        if not dataFromRequest.get('mscp_desc'):
            return False
        if len(dataFromRequest.get('mscp_desc'))<3:
            return False
        if len(dataFromRequest.get('mscp_desc'))>200:
            return False
        return True

    def isParamSearchValid(self, paramFromRequest):
            if not paramFromRequest.get('mscp_id'):
                return False
            return True

    def isParamUpdateValid(self,dataFromRequest):
        if not dataFromRequest.get('mscp_id'):
            return False
        if not dataFromRequest.get('mscp_active_status'):
            return False
        if not  self.isCompanyValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        return self.isCompanyValid(dataFromRequest)

    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)
    # Handle validation