import base64
from datetime import datetime
from ntpath import join
from tarfile import ENCODING
from flask import jsonify, request, send_file
from itsdangerous import exc
from sqlalchemy import true
from sqlalchemy.sql import extract
import xlsxwriter
from io import BytesIO

from application.product_purchased.productPurchasedModel import PurchasedTransactionDetail, PurchasedTransactionHead
from application.product_sold.productSoldModel import SoldTransactionHead
from application.master.product.productModel import Product
from application.master.category_product.categoryProductModel import CategoryProduct
from application.utilities.response import Response



class ReportController:
    def defaultFalse(self):
        return {'status':False, 'msg':'','data':None}

    def exportPurchasedTransaction(self):
        # returning binary file if operation is success, and json instead  if an error is occur

        # try:
        parameterFromRequest=ParameterHandler().getPurchasedParameter()
        isValid=ValidationHandler().isParamValid(parameterFromRequest)

        if not isValid:
            return Response.make(False,'Parameter sended is not valid, process has been canceled.')
        rawDataPurchased=DataHandler().getPurchasedTransaction()

        if not rawDataPurchased:
            return Response.make(False,"There is no data to export")

        excelFile=ExcelWritter().createPurchasedExcel(rawDataPurchased)
        binaryExcelFile=excelFile.read()
        stringExcelFile =base64.b64encode(binaryExcelFile).decode("UTF-8")

        return {'status': True, 'msg':'','data': stringExcelFile }
        # except:
        #     return Response.make(False, "Something wrong while trying to complete the request.")
    def exportSoldTransaction(self):
        return self.defaultFalse()
        # try:
        parameterFromRequest=ParameterHandler().getSoldParameter()
        isValid=ValidationHandler().isParamSoldValid(parameterFromRequest)

        if not isValid:
            return Response.make('Parameter sended is not valid, process has been canceled.')
        rawDataSold=DataHandler().getSoldTransaction(parameterFromRequest)

        isExist=DataHandler().isExist(rawDataSold)
        if not isExist:
            return Response.make(False,"There is no data to export")

        excelFile=ExcelWritter().createSoldExcel(rawDataSold)
        return Response.make(data=excelFile)
        # except:
        #     return Response.make(False, "Something wrong while trying to complete the request.")

class DataHandler:
    def getSoldTransaction(self):
        pass

    def getPurchasedTransaction(self):
        filterStatement=self.getFilterStatementForPurchasedTransaction()
        joinedObject=PurchasedTransactionHead.query.join(PurchasedTransactionDetail).join(Product).join(CategoryProduct)
        return joinedObject.filter(*filterStatement).all()

    def isExist(self):

        pass
    def getFilterStatementForPurchasedTransaction(self):
        parameterFromRequest=ParameterHandler().getPurchasedParameter()
        groupOfFilterStatement=[]

        if parameterFromRequest.get('date_year'):
            tempFilterStatement=(extract('year',PurchasedTransactionHead.tp_date)==parameterFromRequest.get('date_year'),)
            groupOfFilterStatement.append(*tempFilterStatement)

        if parameterFromRequest.get('date_month'):
            tempFilterStatement=(extract('month',PurchasedTransactionHead.tp_date)==parameterFromRequest.get('date_month'),)
            groupOfFilterStatement.append(*tempFilterStatement)

        if parameterFromRequest.get('product_id'):
            tempFilterStatement=(Product.msp_id==parameterFromRequest.get('product_id'),)
            groupOfFilterStatement.append(*tempFilterStatement)

        if parameterFromRequest.get('category_product_id'):
            tempFilterStatement=(CategoryProduct.msc_id==parameterFromRequest.get('category_product_id'),)
            groupOfFilterStatement.append(*tempFilterStatement)
        return tuple(groupOfFilterStatement)

class ParameterHandler:
    def getSoldParameter(self):
        pass

    def getPurchasedParameter(self):
        paramFromRequest={
            'date_year':request.json.get('date_year'),
            'date_month':request.json.get('date_month'),
            'product_id':request.json.get('product_id'),
            'category_product_id':request.json.get('category_id')
        }
        return paramFromRequest
 
class ValidationHandler:
    def isParamValid(self,paramFromRequest):
        if not self.isValidYear(paramFromRequest.get('date_year')):
            return False
        if not self.isValidMonth(paramFromRequest.get('date_month')):
            return False
        if not self.isValidProductId(paramFromRequest.get('product_id')):
            return False
        if not self.isValidCategoryId(paramFromRequest.get('category_product_id')):
            return False
        return True

    def isValidMonth(self, month):

        if not month:
            return True

        if not self.isNumber(month):
            return False
        if  month<0:
            return False
        if month>12:
            return False

        return True

    def isValidYear(self,year):
        if not year:
            return False
        if not self.isNumber(year):
            return False
        if  len(str(year))<4:
            return False
        if  len(str(year))>4:
            return False
        return True

    def isValidProductId(self, productId):
        if not productId:
            return True

        if not self.isNumber(productId):
            return False
        if productId<1:
            return False
        return True

    def isValidCategoryId(self,productCategoryId):
        if not productCategoryId:
            return True

        if not self.isNumber(productCategoryId):
            return False
        if productCategoryId<1:
            return False
        return True
    
    def isParamPurchasedValid(self):
        pass

    def isParamSoldValid(self):
        pass

    def isNumber(self,value):
        try:
            int(value)
            return True
        except:
            return False
    
    
class ExcelWritter:
    def createSoldExcel(self):
        pass
    def createPurchasedExcel(self, rawPuchasedData):
        # we need to write excel inside memory, because server is not allowing apps to write a file inside folders;
        bufferOutput=BytesIO()

        workbook=xlsxwriter.Workbook(bufferOutput)
        excelFormat=self.getExcelFormat(workbook)
        worksheet=workbook.add_worksheet()
        self.writePurchasedData(worksheet,rawPuchasedData,excelFormat)
        workbook.close()

        bufferOutput.seek(0)
        return bufferOutput
        

    def writePurchasedData(self, worksheet,rawPuchasedData, format={}):
        lastCursorPosition=0

        self.writePurchasedExcelTitle({'sheet':worksheet,'format':format}, cursorPosition=0)
        self.writeHeaderForExcelPurchased({'sheet':worksheet, 'format':format},cursorPosition=3)


        for rowLoopNumber,record in enumerate(rawPuchasedData, start=4):
            # set cursor to last Cursor
            cursorPosition=lastCursorPosition+rowLoopNumber

            self.writeHeadOfPurchasedTransaction(
                {'worksheet':worksheet, 'cursorPosition':cursorPosition, 'format':format.get('cellFormat')},
                {'record':record,'index':rowLoopNumber-3})

            for productLoopNumber,detail in enumerate(record.detail_transaction):
                if (productLoopNumber>=1):
                    self.writeEmptyCell(excel)

                excel={'worksheet':worksheet, 'cursorPosition':cursorPosition+productLoopNumber, 'format':format.get('cellFormat')}
                self.writeDetailOfPurchasedTransaction(excel,{'record':detail})

            # save last cursor position to variable cursorPosition
            lastCursorPosition+=len(record.detail_transaction)-1
        
        # set default with of column
        worksheet.set_column(1, 11, 25)

    def writeHeadOfPurchasedTransaction(self,excel,records):
        worksheet=excel.get('worksheet')
        cursorPosition=excel.get('cursorPosition')
        record=records.get('record')
        format=excel.get('format')
        worksheet.write(cursorPosition,0,records.get('index'),format )
        worksheet.write(cursorPosition,1, record.tp_id,format)
        worksheet.write(cursorPosition,2, record.tp_date.strftime('%d/%m/%Y'),format)
        worksheet.write(cursorPosition,3, record.payment_method.mspm_desc,format)
        worksheet.write(cursorPosition,4, record.tp_nominal,format)
        worksheet.write(cursorPosition,5, record.supplier.mssp_desc,format)
        
    def writeEmptyCell(self,excel):
        worksheet=excel.get('worksheet')
        cursorPosition=excel.get('cursorPosition')
        format=excel.get('format')
        for column in range(5):
            worksheet.write(cursorPosition+1, column, '',format)
            
    def writeDetailOfPurchasedTransaction(self,excel,records):
        worksheet=excel.get('worksheet')
        cursorPosition=excel.get('cursorPosition')
        detail=records.get('record')
        format=excel.get('format')

        worksheet.write(cursorPosition, 6,detail.tpd_msp_id,format)
        worksheet.write(cursorPosition, 7,detail.product.msp_desc,format)
        worksheet.write(cursorPosition, 8,detail.product.category_product.msc_desc,format)
        worksheet.write(cursorPosition, 9,detail.tpd_quantity,format)
        worksheet.write(cursorPosition, 10,detail.tpd_msp_price,format)
        worksheet.write(cursorPosition, 11,detail.tpd_msp_price * detail.tpd_quantity,format)
    
    def writeHeaderForExcelPurchased(self,excel,cursorPosition):
        worksheet=excel.get('sheet')
        format=excel.get('format')
        headerExcelOfPurchasedReport=[
        'No','Transaction ID','Purchase Date',
        'Payment method', 'Nominal','Supplier','Product ID', 
        'Description', 'Category Product', 'Quantity', 'Price', 
        'Sub Total'
        ]
        worksheet.write_row(cursorPosition, 0,headerExcelOfPurchasedReport, format.get('headFormat'))
        worksheet.set_row(cursorPosition, 35)

    def writePurchasedExcelTitle(self,excel,cursorPosition):
        worksheet=excel.get('sheet')
        format=excel.get('format')
        title=[
            "Transaction Of Purchased Product",
            "Generated on : "+datetime.now().strftime('%d/%m/%Y %H:%M')
        ]
        worksheet.write_column(cursorPosition, 0,title, format.get('titleFormat'))

    def getExcelFormat(self,workbook):
        headFormat = workbook.add_format({'border': 1,'bold':True, 'font_color': 'white', 'bg_color':'#4bacc6'})
        cellFormat=workbook.add_format({'border': 1})
        titleFormat=workbook.add_format({'bold':true, 'font_size':12})
        groupOfExcelFormat={
            'headFormat':headFormat,
            'cellFormat':cellFormat,
            'titleFormat':titleFormat
        }
        return groupOfExcelFormat
