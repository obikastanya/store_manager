from flask import request
from .companyModel import db,Company, CompanySchema
from application.utilities.response import Response
from sqlalchemy import func

class CompanyController:
    def insert(self):
        data=Company(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'

    def getData(self):
        try:
            companyData,totalRecords, totalRecordsFiltered=DataHandler().grabData()
            return Response.datatable(data={'datas':companyData,'totalRecords':totalRecords,'totalRecordsFiltered':totalRecordsFiltered})
        except:
            return Response.make(status=False,msg='Eror while trying to retrieve data' )
    

class ParameterHandler:
    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='company_id':
            return 'mscp_id'
        if orderColumnName=='category':
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

class DataHandler:
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
        
class ValidationHandler:
    def isValidLimitOffset(self, limit,offset):
        if limit=='' or offset=='':
            return False
        return True
    # Handle validation