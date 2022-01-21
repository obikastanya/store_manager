from flask import request
from application.utilities.response import Response
from .dashboardModel import Dashboard
from calendar import monthrange
from datetime import datetime

class DashboardController():
    def getSummerizeOfTotal(self):
        try:
            parameterFromRequest=ParameterHandler().getParameter()
            rawSummaryTotalData=Dashboard().getSummaryOfTotal(parameterFromRequest)
            dictOfSummaryTotal=DashboardDataMapper.mapSummaryOfTotal(rawSummaryTotalData)
            return Response.make(data=[dictOfSummaryTotal])
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")
        
    def getSummerizeOfPurchasedVsSoldProduct(self):
        try:
            rawSummaryPurchasedVsSold=DataHandler().getSummaryOfPurchasedVsSold()
            dictOfSummaryPurchasedVsSold=DashboardDataMapper.mapSummaryOfPurchasedVsSold(rawSummaryPurchasedVsSold)
            if not dictOfSummaryPurchasedVsSold:
                return Response.make(False,"Data is not found")
            return Response.make(data=dictOfSummaryPurchasedVsSold)
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")

    def getSummerizeOfPurchasedVsSoldProductByCategory(self):
        try:
            rawSummaryPurchasedVsSold=DataHandler().getSummaryOfPurchasedVsSoldByCategory()
            dictOfSummaryPurchasedVsSold=DashboardDataMapper.mapSummaryOfPurchasedVsSoldByCategory(rawSummaryPurchasedVsSold)
            if not dictOfSummaryPurchasedVsSold:
                return Response.make(False,"Data is not found")
            return Response.make(data=dictOfSummaryPurchasedVsSold)
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")
        
    def getSummerizeOfSoldProduct(self):
        try:
            rawSummarySold=DataHandler().getSummaryOfSold()
            dictOfSummarySold=DashboardDataMapper.mapSummaryOfSold(rawSummarySold)
            if not dictOfSummarySold:
                return Response.make(False,"Data is not found")
            return Response.make(data=dictOfSummarySold)
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")

    def getSummerizeOfSoldProductByCategory(self):
        try:
            rawSummarySold=DataHandler().getSummaryOfSoldByCategory()
            dictOfSummarySold=DashboardDataMapper.mapSummaryOfSoldByCategory(rawSummarySold)
            if not dictOfSummarySold:
                return Response.make(False,"Data is not found")
            return Response.make(data=dictOfSummarySold)
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")
        
    def getSummerizeOfPurchasedProduct(self):
        try:
            rawSummaryPurchased=DataHandler().getSummaryOfPurchased()
            dictOfSummaryPurchased=DashboardDataMapper.mapSummaryOfPurchased(rawSummaryPurchased)
            if not dictOfSummaryPurchased:
                return Response.make(False,"Data is not found")
            return Response.make(data=dictOfSummaryPurchased)
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")

    def getSummerizeOfPurchasedProductByCategory(self):
        try:
            rawSummaryPurchased=DataHandler().getSummaryOfPurchasedByCategory()
            dictOfSummaryPurchased=DashboardDataMapper.mapSummaryOfPurchasedByCategory(rawSummaryPurchased)
            if not dictOfSummaryPurchased:
                return Response.make(False,"Data is not found")
            return Response.make(data=dictOfSummaryPurchased)
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")
        
    def getSummerizeOfStoreAvailability(self):
        try:
            rawSummaryAvailability=Dashboard().getSummaryOfAvailabilityStore()
            dictOfSummaryAvailability=DashboardDataMapper.mapSummaryOfAvailability(rawSummaryAvailability)
            if not dictOfSummaryAvailability:
                return Response.make(False,"Data is not found")
            return Response.make(data=dictOfSummaryAvailability)
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")
        
    def getSummerizeOfWarehouseAvailability(self):
        try:
            rawSummaryAvailability=Dashboard().getSummaryOfAvailabilityWarehouse()
            dictOfSummaryAvailability=DashboardDataMapper.mapSummaryOfAvailability(rawSummaryAvailability)
            if not dictOfSummaryAvailability:
                return Response.make(False,"Data is not found")
            return Response.make(data=dictOfSummaryAvailability)
        except:
            return Response.make(False, "Something wrong while trying to complete the request.")

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

        if isDateMonthExist and isDateYearExist :
            numberOfDays=ParameterHandler().getNumberOfDateInMonth(parameterFromRequest.get('date_year'),parameterFromRequest.get('date_month'))
            parameterFromRequest.update({'number_date_in_month':numberOfDays})
            return Dashboard().getSummaryOfPurchasedVsSoldInMonth(parameterFromRequest)
        else:
            numberOfDays=ParameterHandler().getNumberOfDateInYear(parameterFromRequest.get('date_year'),parameterFromRequest.get('date_month'))
            parameterFromRequest.update({'number_date_in_month':numberOfDays})
            
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

        if isDateMonthExist and isDateYearExist :
            numberOfDays=ParameterHandler().getNumberOfDateInMonth(parameterFromRequest.get('date_year'),parameterFromRequest.get('date_month'))
            parameterFromRequest.update({'number_date_in_month':numberOfDays})
            return Dashboard().getSummaryOfSoldInMonth(parameterFromRequest)
        else:
            numberOfDays=ParameterHandler().getNumberOfDateInYear(parameterFromRequest.get('date_year'),parameterFromRequest.get('date_month'))
            parameterFromRequest.update({'number_date_in_month':numberOfDays})
            return Dashboard().getSummaryOfSoldInYear(parameterFromRequest)

    def getSummaryOfPurchasedByCategory(self):
        parameterFromRequest=ParameterHandler().getParameter()
        isDateMonthExist=bool(parameterFromRequest.get('date_month'))
        isDateYearExist=bool(parameterFromRequest.get('date_year'))

        if isDateMonthExist and isDateYearExist:
            return Dashboard().getSummaryOfPurchasedGroupByCategoryInMonth(parameterFromRequest)
        return Dashboard().getSummaryOfPurchasedGroupByCategoryInYear(parameterFromRequest)

    def getSummaryOfPurchased(self):
        parameterFromRequest=ParameterHandler().getParameter()
        isDateMonthExist=bool(parameterFromRequest.get('date_month'))
        isDateYearExist=bool(parameterFromRequest.get('date_year'))

        if isDateMonthExist and isDateYearExist :
            numberOfDays=ParameterHandler().getNumberOfDateInMonth(parameterFromRequest.get('date_year'),parameterFromRequest.get('date_month'))
            parameterFromRequest.update({'number_date_in_month':numberOfDays})
            return Dashboard().getSummaryOfPurchasedInMonth(parameterFromRequest)
        else:
            numberOfDays=ParameterHandler().getNumberOfDateInYear(parameterFromRequest.get('date_year'),parameterFromRequest.get('date_month'))
            parameterFromRequest.update({'number_date_in_month':numberOfDays})
            return Dashboard().getSummaryOfPurchasedInYear(parameterFromRequest)
 
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
                'data_value':record[1],
                'data_key':record[0]
            }
            dictOfSummaryPuchasedVsSold.append(dictRecord)
        return dictOfSummaryPuchasedVsSold
    @staticmethod
    def mapSummaryOfSold(rawData):
        dictOfSummaryPuchasedVsSold=[]
        for record in rawData:
            dictRecord={
                'data_value':record[1],
                'data_key':record[0]
            }
            dictOfSummaryPuchasedVsSold.append(dictRecord)
        return dictOfSummaryPuchasedVsSold

    @staticmethod
    def mapSummaryOfSoldByCategory(rawData):
        dictOfSummaryPuchasedVsSold=[]
        for record in rawData:
            dictRecord={
                'data_value':record[1],
                'data_key':record[0]
            }
            dictOfSummaryPuchasedVsSold.append(dictRecord)
        return dictOfSummaryPuchasedVsSold

    @staticmethod
    def mapSummaryOfPurchased(rawData):
        dictOfSummaryPuchasedVsPurchased=[]
        for record in rawData:
            dictRecord={
                'data_value':record[1],
                'data_key':record[0]
            }
            dictOfSummaryPuchasedVsPurchased.append(dictRecord)
        return dictOfSummaryPuchasedVsPurchased

    @staticmethod
    def mapSummaryOfPurchasedByCategory(rawData):
        dictOfSummaryPuchasedVsPurchased=[]
        for record in rawData:
            dictRecord={
                'data_value':record[1],
                'data_key':record[0]
            }
            dictOfSummaryPuchasedVsPurchased.append(dictRecord)
        return dictOfSummaryPuchasedVsPurchased
    @staticmethod
    def mapSummaryOfAvailability(rawData):
        dictOfSummaryPuchasedVsPurchased=[]
        for record in rawData:
            dictRecord={
                'data_value':record[1],
                'data_key':record[0]
            }
            dictOfSummaryPuchasedVsPurchased.append(dictRecord)
        return dictOfSummaryPuchasedVsPurchased
       
class ParameterHandler:
    def getParameter(self):
        dictParameter={
        'date_month':request.json.get('date_month'),
        'date_year':self.getDateYear(),
        'summarize_type':request.json.get('summarize_type'),
        'group_by_category':request.json.get('group_by_category')
        }
        return dictParameter

    def getDateYear(self):
        if not request.json.get('date_year'):
            return datetime.now().year
        return request.json.get('date_year')

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
    
    