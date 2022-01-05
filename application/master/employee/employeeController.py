import re
from flask import request
from sqlalchemy import func
from .employeeModel import db,Employee,EmployeeSchema
from ..baseMasterController import MasterController, DataHandler, ParameterHandler, ValidationHandler
from application.utilities.response import Response

class EmployeeController(MasterController):
    def __init__(self):
        super().__init__()
        self.dataHandler=DataHandlerImpl()
        self.validationHandler=ValidationHandlerImpl()
        self.parameterHandler=ParameterHandlerImpl()

    def getLovData(self):
        # try:
        data=self.dataHandler.grabLovData()
        return Response.make(msg='Data found',data=data)
        # except:
        #     return Response.make(status=False,msg='Eror while trying to retrieve data' )

class DataHandlerImpl(DataHandler):
    def __init__(self):
        super().__init__()
        self.Model=Employee
        self.Schema=EmployeeSchema
        self.parameterHandler=ParameterHandlerImpl()


    def updateData(self, dataFromRequest):
        employee=self.grabOne(dataFromRequest)
        employee.msse_id=dataFromRequest.get('msse_id')
        employee.mse_name=dataFromRequest.get('mse_name')
        employee.mse_phone_number=dataFromRequest.get('mse_phone_number')
        employee.mse_email=dataFromRequest.get('mse_email')
        employee.mse_address=dataFromRequest.get('mse_address')
        employee.mse_salary=dataFromRequest.get('mse_salary')
        employee.mse_position=dataFromRequest.get('mse_position')
        employee.mse_start_working=dataFromRequest.get('mse_start_working')
        employee.mse_end_working=dataFromRequest.get('mse_end_working')
        db.session.commit()
    
    def grabLovData(self):
        groupOfObjectResult=self.Model.query.filter(self.Model.mse_end_working==None).all()
        return self.Schema(many=True).dump(groupOfObjectResult)

    def grabOne(self, paramFromRequest):
        return self.Model.query.filter_by(mse_id=paramFromRequest.get('mse_id')).first()

    def grabTotalRecords(self):
        return db.session.query(func.count(self.Model.mse_id)).scalar()

    def grabTotalRecordsFiltered(self, datatableConfig):
        searchKeyWord=self.getSearchKeywordStatement(datatableConfig)
        return db.session.query(func.count(self.Model.mse_id)).filter(searchKeyWord ).scalar()

    def getSearchKeywordStatement(self, datatableConfig):
        return self.Model.mse_name.like("%{}%".format(datatableConfig.get('searchKeyWord')))
    
    def getOrderStatement(self,datatableConfig):
        orderStatement=None
        columnToOrder=datatableConfig.get('orderBy')
        orderDirection=datatableConfig.get('orderDirection')

        if columnToOrder=='mse_id': 
            orderStatement=self.getOrderDirectionById(orderDirection)
        elif columnToOrder=='msse_id':
            orderStatement=self.getOrderDirectionByStatusEmployeeId(orderDirection)
        elif columnToOrder=='mse_name':
            orderStatement=self.getOrderDirectionByName(orderDirection)
        elif columnToOrder=='mse_phone_number':
            orderStatement=self.getOrderDirectionByPhoneNumber(orderDirection)
        elif columnToOrder=='mse_email':
            orderStatement=self.getOrderDirectionByEmail(orderDirection)
        elif columnToOrder=='mse_address':
            orderStatement=self.getOrderDirectionByAddress(orderDirection)
        elif columnToOrder=='mse_salary':
            orderStatement=self.getOrderDirectionBySalary(orderDirection)
        elif columnToOrder=='mse_position':
            orderStatement=self.getOrderDirectionByPosition(orderDirection)
        elif columnToOrder=='mse_start_working':
            orderStatement=self.getOrderDirectionByStartWorking(orderDirection)
        elif columnToOrder=='mse_end_working':
            orderStatement=self.getOrderDirectionByEndWorking(orderDirection)
        return orderStatement

    def getOrderDirectionById(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mse_id.desc()
        return self.Model.mse_id.asc()

    def getOrderDirectionByStatusEmployeeId(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.msse_id.desc()
        return self.Model.msse_id.asc()
    
    def getOrderDirectionByName(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mse_name.desc()
        return self.Model.mse_name.asc()
    
    def getOrderDirectionByPhoneNumber(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mse_email.desc()
        return self.Model.mse_email.asc()
    
    def getOrderDirectionByEmail(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mse_address.desc()
        return self.Model.mse_address.asc()
    
    def getOrderDirectionBySalary(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mse_salary.desc()
        return self.Model.mse_salary.asc()

    def getOrderDirectionByPosition(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mse_position.desc()
        return self.Model.mse_position.asc()
    
    def getOrderDirectionByStartWorking(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mse_start_working.desc()
        return self.Model.mse_start_working.asc()
    
    def getOrderDirectionByEndWorking(self, orderDirection):
        if orderDirection=='desc':
            return self.Model.mse_end_working.desc()
        return self.Model.mse_end_working.asc()

class ParameterHandlerImpl(ParameterHandler):
    def getParamInsertFromRequests(self):
        dataFromRequest={
            'msse_id':request.json.get('employee_status_id'),
            'mse_name':request.json.get('name'),
            'mse_phone_number':request.json.get('phone_number'),
            'mse_email':request.json.get('email'),
            'mse_address':request.json.get('address'),
            'mse_salary':request.json.get('salary'),
            'mse_position':request.json.get('position'),
            'mse_start_working':request.json.get('start_working')
        }
        return dataFromRequest

    def getUpdateValuesFromRequests(self):
        dataFromRequest={
            'mse_id':request.json.get('employee_id'),
            'msse_id':request.json.get('employee_status_id'),
            'mse_name':request.json.get('name'),
            'mse_phone_number':request.json.get('phone_number'),
            'mse_email':request.json.get('email'),
            'mse_address':request.json.get('address'),
            'mse_salary':request.json.get('salary'),
            'mse_position':request.json.get('position'),
            'mse_start_working':request.json.get('start_working'),
            'mse_end_working':self.getEndWorkingOrNone()
        }
        return dataFromRequest
        
    def getEndWorkingOrNone(self):
        if not request.json.get('end_working'):
            return None
        return request.json.get('end_working')


    def getIdFromRequest(self):
        parameterFromRequest={
            'mse_id':request.json.get('employee_id')
        }
        return parameterFromRequest

    def getOrderColumnName(self):
        orderColumnIndex=request.args.get('order[0][column]','')
        orderColumnName=request.args.get('columns[%s][name]'%orderColumnIndex,'')
        if orderColumnName=='employee_id':
            return 'mse_id'
        if orderColumnName=='employee_status_id':
            return 'msse_id'
        if orderColumnName=='name':
            return 'mse_name'
        if orderColumnName=='phone_number':
            return 'mse_phone_number'
        if orderColumnName=='email':
            return 'mse_email'
        if orderColumnName=='address':
            return 'mse_address'
        if orderColumnName=='salary':
            return 'mse_salary'
        if orderColumnName=='position':
            return 'mse_position'
        if orderColumnName=='start_working':
            return 'mse_start_working'
        if orderColumnName=='end_working':
            return 'mse_end_working'
        return None

class ValidationHandlerImpl(ValidationHandler):
    def isParamSearchValid(self, paramFromRequest):
            if not paramFromRequest.get('mse_id'):
                return False
            return True

    def isParamUpdateValid(self,dataFromRequest):
        if not self.isIdValid(dataFromRequest):
            return False
        if not self.isParamInsertValid(dataFromRequest):
            return False
        return True

    def isParamInsertValid(self, dataFromRequest):
        if not self.isStatusEmployeeValid(dataFromRequest):
            return False
        if not self.isNameValid(dataFromRequest):
            return False
        if not self.isPhoneNumberValid(dataFromRequest):
            return False
        if not self.isEmailValid(dataFromRequest):
            return False
        if not self.isAddressValid(dataFromRequest):
            return False
        if not self.isSalaryValid(dataFromRequest):
            return False
        if not self.isPositionValid(dataFromRequest):
            return False
        if not self.isStartWorkingValid(dataFromRequest):
            return False
        return True
    def isIdValid(self,dataFromRequest):
        if not dataFromRequest.get('mse_id'):
            return False
        if not self.isNumber(dataFromRequest.get('mse_id')):
            return False
        return True
    def isStatusEmployeeValid(self, dataFromRequest):
        if not dataFromRequest.get('msse_id'):
            return False
        if not self.isNumber(dataFromRequest.get('msse_id')):
            return False
        return True

    def isNameValid(self,dataFromRequest):
        if not dataFromRequest.get('mse_name'):
            return False
        if len(dataFromRequest.get('mse_name'))<3:
            return False
        if len(dataFromRequest.get('mse_name'))>200:
            return False
        return True

    def isPhoneNumberValid(self,dataFromRequest):
        if not dataFromRequest.get('mse_phone_number'):
            return False
        if len(dataFromRequest.get('mse_phone_number'))<3:
            return False
        if len(dataFromRequest.get('mse_phone_number'))>30:
            return False
        return True

    def isEmailValid(self, dataFromRequest):
        if not dataFromRequest.get('mse_email'):
            return False
        if len(dataFromRequest.get('mse_email'))<3:
            return False
        if len(dataFromRequest.get('mse_email'))>100:
            return False
        if not self.isMatchPatternEmail(dataFromRequest.get('mse_email')):
            return False
        return True

    def isAddressValid(self, dataFromRequest):
        if not dataFromRequest.get('mse_address'):
            return False
        if len(dataFromRequest.get('mse_address'))<5:
            return False
        if len(dataFromRequest.get('mse_address'))>200:
            return False
        return True

    def isSalaryValid(self, dataFromRequest):
        if not dataFromRequest.get('mse_salary'):
            return False
        if len(str(dataFromRequest.get('mse_salary')))<2:
            return False
        if len(str(dataFromRequest.get('mse_salary')))>12:
            return False
        if not self.isNumber(dataFromRequest.get('mse_salary')):
            return False
        return True

    def isPositionValid(self,dataFromRequest):
        if not dataFromRequest.get('mse_position'):
            return False
        if len(dataFromRequest.get('mse_position'))<3:
            return False
        if len(dataFromRequest.get('mse_position'))>100:
            return False
        return True

    def isStartWorkingValid(self,dataFromRequest):
        if not dataFromRequest.get('mse_start_working'):
            return False
        return True

    def isEndWorkingValid(self,dataFromRequest):
        if not dataFromRequest.get('mse_end_working'):
            return False
        return True
    
    def isMatchPatternEmail(self,value):
        emailPattern= r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(emailPattern,value)):
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

    def isParamDeleteValid(self, paramFromRequest):
        return self.isParamSearchValid(paramFromRequest)

    