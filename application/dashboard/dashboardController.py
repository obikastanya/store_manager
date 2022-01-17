from flask import request
from application.utilities.response import Response
from .dashboardModel import Dashboard
from calendar import monthrange
from datetime import datetime

class DashboardController():
    def getSummerizeOfTotal(self):
        # try:
        parameterFromRequest=ParameterHandler().getParameter()
        rawSummaryTotalData=Dashboard().getSummaryOfTotal(parameterFromRequest)
        dictOfSummaryTotal=DashboardDataMapper.mapSummaryOfTotal(rawSummaryTotalData)
        return Response.make(data=[dictOfSummaryTotal])
        # except:
        #     return Response.make(False, "Something wrong while trying to complete the request.")
        
    def getSummerizeOfPurchasedVsSoldProduct(self):
        # try:
        rawSummaryPurchasedVsSold=DataHandler().getSummaryOfPurchasedVsSold()
        dictOfSummaryPurchasedVsSold=DashboardDataMapper.mapSummaryOfPurchasedVsSold(rawSummaryPurchasedVsSold)
        if not dictOfSummaryPurchasedVsSold:
            return Response.make(False,"Data is not found")
        return Response.make(data=dictOfSummaryPurchasedVsSold)
        # except:
            # return Response.make(False, "Something wrong while trying to complete the request.")

    def getSummerizeOfPurchasedVsSoldProductByCategory(self):
        # try:
        rawSummaryPurchasedVsSold=DataHandler().getSummaryOfPurchasedVsSoldByCategory()
        dictOfSummaryPurchasedVsSold=DashboardDataMapper.mapSummaryOfPurchasedVsSoldByCategory(rawSummaryPurchasedVsSold)
        if not dictOfSummaryPurchasedVsSold:
            return Response.make(False,"Data is not found")
        return Response.make(data=dictOfSummaryPurchasedVsSold)
        # except:
            # return Response.make(False, "Something wrong while trying to complete the request.")
        
    def getSummerizeOfSoldProduct(self):
        # try:
        rawSummarySold=DataHandler().getSummaryOfSold()
        dictOfSummarySold=DashboardDataMapper.mapSummaryOfSold(rawSummarySold)
        if not dictOfSummarySold:
            return Response.make(False,"Data is not found")
        return Response.make(data=dictOfSummarySold)
        # except:
            # return Response.make(False, "Something wrong while trying to complete the request.")

    def getSummerizeOfSoldProductByCategory(self):
        # try:
        rawSummarySold=DataHandler().getSummaryOfPurchasedVsSoldByCategory()
        dictOfSummarySold=DashboardDataMapper.mapSummaryOfSoldByCategory(rawSummarySold)
        if not dictOfSummarySold:
            return Response.make(False,"Data is not found")
        return Response.make(data=dictOfSummarySold)
        # except:
            # return Response.make(False, "Something wrong while trying to complete the request.")
        
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

class DataHandler:
    def getSummaryOfPurchasedVsSoldByCategory(self):
        parameterFromRequest=ParameterHandler().getParameter()
        isDateMonthExist=bool(parameterFromRequest.get('date_month'))
        isDateYearExist=bool(parameterFromRequest.get('date_year'))

        if isDateMonthExist and isDateYearExist:
            return Dashboard().getSummaryOfPurchasedVsSoldGroupByCategoryInMonth(parameterFromRequest)
        # if  years is the only param exist
        return Dashboard().getSummaryOfPurchasedVsSoldGroupByCategoryInYear(parameterFromRequest)

    def getSummaryOfPurchasedVsSold(self):
        parameterFromRequest=ParameterHandler().getParameter()
        isDateMonthExist=bool(parameterFromRequest.get('date_month'))
        isDateYearExist=bool(parameterFromRequest.get('date_year'))

        numberOfDays=ParameterHandler().getNumberOfDateInMonth(parameterFromRequest.get('date_year'),parameterFromRequest.get('date_month'))
        parameterFromRequest.update({'number_date_in_month':numberOfDays})

        # get data for  monthly or yearly statistic group by date
        if isDateMonthExist and isDateYearExist :
            return Dashboard().getSummaryOfPurchasedVsSoldInMonth(parameterFromRequest)
        return Dashboard().getSummaryOfPurchasedVsSoldInYear(parameterFromRequest)

    def getSummaryOfSoldByCategory(self):
        parameterFromRequest=ParameterHandler().getParameter()
        isDateMonthExist=bool(parameterFromRequest.get('date_month'))
        isDateYearExist=bool(parameterFromRequest.get('date_year'))

        if isDateMonthExist and isDateYearExist:
            return Dashboard().getSummaryOfSoldGroupByCategoryInMonth(parameterFromRequest)
        return Dashboard().getSummaryOfSoldGroupByCategoryInYear(parameterFromRequest)

    def getSummaryOfSold(self):
        parameterFromRequest=ParameterHandler().getParameter()
        isDateMonthExist=bool(parameterFromRequest.get('date_month'))
        isDateYearExist=bool(parameterFromRequest.get('date_year'))

        numberOfDays=ParameterHandler().getNumberOfDateInMonth(parameterFromRequest.get('date_year'),parameterFromRequest.get('date_month'))
        parameterFromRequest.update({'number_date_in_month':numberOfDays})

        if isDateMonthExist and isDateYearExist :
            return Dashboard().getSummaryOfSoldInMonth(parameterFromRequest)
        return Dashboard().getSummaryOfSoldInYear(parameterFromRequest)
 

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

    @staticmethod
    def mapSummaryOfPurchasedVsSoldByCategory(rawData):
        dictOfSummaryPuchasedVsSold=[]
        for record in rawData:
            dictRecord={
                'data_value':record[0],
                'data_key':record[1]
            }
            dictOfSummaryPuchasedVsSold.append(dictRecord)
        return dictOfSummaryPuchasedVsSold
    @staticmethod
    def mapSummaryOfSold(rawData):
        dictOfSummaryPuchasedVsSold=[]
        for record in rawData:
            dictRecord={
                'data_value':record[0],
                'data_key':record[1]
            }
            dictOfSummaryPuchasedVsSold.append(dictRecord)
        return dictOfSummaryPuchasedVsSold

    @staticmethod
    def mapSummaryOfSoldByCategory(rawData):
        dictOfSummaryPuchasedVsSold=[]
        for record in rawData:
            dictRecord={
                'data_value':record[0],
                'data_key':record[1]
            }
            dictOfSummaryPuchasedVsSold.append(dictRecord)
        return dictOfSummaryPuchasedVsSold
       
class ParameterHandler:
    def getParameter(self):
        dictParameter={
        'date_month':request.args.get('date_month'),
        'date_year':self.getDateYear(),
        'summarize_type':request.args.get('summarize_type'),
        'group_by_category':request.args.get('group_by_category')
        }
        return dictParameter

    def getDateYear(self):
        if not request.args.get('date_year'):
            return datetime.now().year
        return request.args.get('date_year')

    def getNumberOfDateInMonth(self, year, month):
        currentYear=datetime.now().year
        currentMonth=datetime.now().month
        
        if not month:
            month=datetime.now().month

        # check if the its current time
        if currentYear==int(year) and currentMonth==int(month):
            return datetime.now().day

        numberOfDays=monthrange(int(year),int(month))
        return numberOfDays[1]
    
    def getNumberOfDateInYear(self, year, month):
        
        currentYear=datetime.now().year
        currentMonth=datetime.now().month

        # check if the its current time
        if not month:
            month=datetime.now().month

        if currentYear==int(year) and currentMonth==int(month):
            return datetime.now().month
        return 12
    
    