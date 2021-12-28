from flask import request
from .productSoldModel import SoldTransactionHead,SoldTransactionDetail, SoldTransactionDetailDiscountApplied
from .productSoldModel import SoldTransactionHeadSchema,SoldTransactionDetailSchema, SoldTransactionDetailDiscountAppliedSchema
from application.utilities.response import Response

class ProductSoldController:
    def defaultFalse(self):
        return {'status':False,'msg':'default false msg'}
    def getData(self):
        return self.defaultFalse()
    def insertNewTransaction(self):
        return self.defaultFalse()
    def deleteTransaction(self):
        return self.defaultFalse()
    def filterTransaction(self):
        return self.defaultFalse()
    def searchDetailTransaction(self):
        return self.defaultFalse()

class DataHandlerImpl:
    pass
class ParameterHandlerImpl:
    pass
class ValidationHandlerImpl:
    pass