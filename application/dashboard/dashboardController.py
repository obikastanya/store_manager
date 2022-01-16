from flask import request
from application.utilities.response import Response
from .dashboardModel import Dashboard
from calendar import monthrange
from datetime import datetime

class DashboardController():
    def getSummerizeOfTotal(self):
        try:
            rawSummaryTotalData=Dashboard().getSummaryOfTotal({})
            dictOfSummaryTotal=DashboardDataMapper.mapSummaryOfTotal(rawSummaryTotalData)
            return Response.make(data=[dictOfSummaryTotal])
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")
        
    def getSummerizeOfPurchasedVsSoldProduct(self):
        # try:
        rawSummaryPurchasedVsSold=DataHandler().getSummaryOfPurchasedVsSold()
        dictOfSummaryPurchasedVsSold=DashboardDataMapper.mapSummaryOfPurchasedVsSold(rawSummaryPurchasedVsSold)
        if not dictOfSummaryPurchasedVsSold:
            return Response.make(False,"Data is not found")
        return Response.make(data=dictOfSummaryPurchasedVsSold)
        # except:
            # return Response.make(False, "Something wrong while trying to complete the request.")
    def getSummerizeOfSoldTransaction(self):
        return self.defaultFalse()
    def getSummerizeOfPurchasedTransaction(self):
        return self.defaultFalse()
    def getSummerizeOfStoreAvailability(self):
        return self.defaultFalse()
    def getSummerizeOfWarehouseAvailability(self):
        return self.defaultFalse()

    def requestIsNotRecognize(self):
        return Response.make(False,"Request is not recognized")

    def defaultFalse(self):
        return Response.make(False)

class DashboardDataMapper:
    @staticmethod
    def mapSummaryOfTotal(rawData):
        dictOfSummaryTotal={
        'total_cash_out':rawData[0],
        'total_transaction_product_sold':rawData[1],
        'total_cash_in':rawData[2],
        'total_transaction_product_purchased':rawData[3],
        'total_product_in_store':rawData[4]
        }
        return dictOfSummaryTotal

    def mapSummaryOfPurchasedVsSold(rawData):
        dictOfSummaryPuchasedVsSold=[]
        for record in rawData:
            dictRecord={
                'date_sold':record[0],
                'product_sold':record[1],
                'product_purchased':record[2],
            }
            dictOfSummaryPuchasedVsSold.append(dictRecord)
        return dictOfSummaryPuchasedVsSold

class DataHandler:
    def getSummaryOfPurchasedVsSold(self):
        parameterFromRequest=ParameterHandler().getParameter()
        if parameterFromRequest.get('date_month') and parameterFromRequest.get('date_year'):
            numberOfDays=ParameterHandler().getNumberOfDateInMonth(parameterFromRequest.get('date_year'),parameterFromRequest.get('date_month'))
            parameterFromRequest.update({'number_date_in_month':numberOfDays})
            return Dashboard().getSummaryOfPurchasedVsSold(parameterFromRequest)
        return []

class ParameterHandler:
    def getParameter(self):
        dictParameter={
        'date_month':request.args.get('date_month'),
        'date_year':request.args.get('date_year'),
        'summarize_type':request.args.get('summarize_type'),
        'group_by_category':request.args.get('group_by_category')
        }
        return dictParameter

    def getNumberOfDateInMonth(self, year, month):
        currentYear=datetime.now().year
        currentMonth=datetime.now().month

        # check if the its current time
        if currentYear==int(year) and currentMonth==int(month):
            return datetime.now().day

        numberOfDays=monthrange(int(year),int(month))
        return numberOfDays[1]
    