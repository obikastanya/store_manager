import base64
from datetime import datetime
from flask import request
from sqlalchemy import true
from sqlalchemy.sql import extract
import xlsxwriter
from io import BytesIO

from application.product_purchased.productPurchasedModel import PurchasedTransactionDetail, PurchasedTransactionHead
from application.product_sold.productSoldModel import SoldTransactionDetail, SoldTransactionHead
from application.master.product.productModel import Product
from application.master.category_product.categoryProductModel import CategoryProduct
from application.utilities.response import Response



class ReportController:

    def exportPurchasedTransaction(self):
        # returning binary file if operation is success, and json instead  if an error is occur
        # try:
        parameterFromRequest=ParameterHandler().getParameter()
        isValid=ValidationHandler().isParamValid(parameterFromRequest)

        if not isValid:
            return Response.make(False,'Parameter sended is not valid, process has been canceled.')
        rawDataPurchased=DataHandler().getPurchasedTransaction()

        if not rawDataPurchased:
            return Response.make(False,"There is no data to export")

        # convert excel to base64 string so we could include them inside json
        excelFile=ExcelWritter().createPurchasedExcel(rawDataPurchased)
        binaryExcelFile=excelFile.read()
        stringExcelFile =base64.b64encode(binaryExcelFile).decode("UTF-8")

        return {'status': True, 'msg':'','data': stringExcelFile }
        # except:
        #     return Response.make(False, "Something wrong while trying to complete the request.")
    def exportSoldTransaction(self):
        # try:
        parameterFromRequest=ParameterHandler().getParameter()
        isValid=ValidationHandler().isParamValid(parameterFromRequest)

        if not isValid:
            return Response.make(False,'Parameter sended is not valid, process has been canceled.')
        rawDataSold=DataHandler().getSoldTransaction()

        if not rawDataSold:
            return Response.make(False,"There is no data to export")

        excelFile=ExcelWritter().createSoldExcel(rawDataSold)
        binaryExcelFile=excelFile.read()
        stringExcelFile =base64.b64encode(binaryExcelFile).decode("UTF-8")

        return {'status': True, 'msg':'','data': stringExcelFile }
        # except:
        #     return Response.make(False, "Something wrong while trying to complete the request.")

class DataHandler:
    def getSoldTransaction(self):
        filterStatement=self.getFilterStatementForSoldTransaction()
        joinedObject=SoldTransactionHead.query.join(SoldTransactionDetail).join(Product).join(CategoryProduct)
        return joinedObject.filter(*filterStatement).all()

    def getPurchasedTransaction(self):
        filterStatement=self.getFilterStatementForPurchasedTransaction()
        joinedObject=PurchasedTransactionHead.query.join(PurchasedTransactionDetail).join(Product).join(CategoryProduct)
        return joinedObject.filter(*filterStatement).all()

    def getFilterStatementForPurchasedTransaction(self):
        parameterFromRequest=ParameterHandler().getParameter()
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

    def getFilterStatementForSoldTransaction(self):
        parameterFromRequest=ParameterHandler().getParameter()
        groupOfFilterStatement=[]

        if parameterFromRequest.get('date_year'):
            tempFilterStatement=(extract('year',SoldTransactionHead.th_date)==parameterFromRequest.get('date_year'),)
            groupOfFilterStatement.append(*tempFilterStatement)

        if parameterFromRequest.get('date_month'):
            tempFilterStatement=(extract('month',SoldTransactionHead.th_date)==parameterFromRequest.get('date_month'),)
            groupOfFilterStatement.append(*tempFilterStatement)

        if parameterFromRequest.get('product_id'):
            tempFilterStatement=(Product.msp_id==parameterFromRequest.get('product_id'),)
            groupOfFilterStatement.append(*tempFilterStatement)

        if parameterFromRequest.get('category_product_id'):
            tempFilterStatement=(CategoryProduct.msc_id==parameterFromRequest.get('category_product_id'),)
            groupOfFilterStatement.append(*tempFilterStatement)
        return tuple(groupOfFilterStatement)

class ParameterHandler:

    def getParameter(self):
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
    
    def isNumber(self,value):
        try:
            int(value)
            return True
        except:
            return False
    
    
class ExcelWritter:
    def createSoldExcel(self, rawSoldData):
        bufferOutput=BytesIO()

        workbook=xlsxwriter.Workbook(bufferOutput)
        excelFormat=self.getExcelFormat(workbook)
        worksheet=workbook.add_worksheet()
        self.writeSoldData(worksheet,rawSoldData,excelFormat)
        workbook.close()

        bufferOutput.seek(0)
        return bufferOutput

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
    
    def writeSoldData(self, worksheet,rawSoldData, format={}):
        lastCursorPosition=0

        self.writeSoldExcelTitle({'sheet':worksheet,'format':format}, cursorPosition=0)
        self.writeHeaderForExcelSold({'sheet':worksheet, 'format':format},cursorPosition=3)
        for rowLoopNumber,record in enumerate(rawSoldData, start=4):
            cursorPosition=lastCursorPosition+rowLoopNumber
            self.writeHeadExcelOfSoldTransaction(
                {'sheet':worksheet,'cursorPosition':cursorPosition,'format':format.get('cellFormat')},
                {'record':record,'index':rowLoopNumber-3})
            
            for productLoopNumber,detail in enumerate(record.detail_transaction):
                excel={'worksheet':worksheet, 'cursorPosition':cursorPosition+productLoopNumber, 'format':format.get('cellFormat')}
                
                
                self.writeDetailExcelOfSoldTransaction(excel,{'record':detail})
            
                if detail.detail_discount_applied:
                    for discountLoopNumber,discountApplied in enumerate(detail.detail_discount_applied):
                        excel={'worksheet':worksheet, 'cursorPosition':cursorPosition+productLoopNumber+discountLoopNumber, 'format':format.get('cellFormat')}
                        if (discountLoopNumber>=1):
                            self.writeEmptyCellSoldDetail(excel)

                        self.writeDiscountAppliedOnSoldTransaction(excel,{'record':discountApplied})
                    lastCursorPosition+=len(detail.detail_discount_applied)-1
                    
                else:
                    worksheet.write_row(cursorPosition+productLoopNumber,12,["","",""],format.get('cellFormat'))
                    
            lastCursorPosition+=len(record.detail_transaction)-1
            
            # write border for empty space on head transaction data
            
            if (rowLoopNumber+lastCursorPosition !=cursorPosition ):
                for row in range(cursorPosition,rowLoopNumber+lastCursorPosition):
                    excel={'worksheet':worksheet, 'cursorPosition':row, 'format':format.get('cellFormat')}
                    self.writeEmptyCellSold(excel)
        worksheet.set_column(1, 14, 20)

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
        
        # set default width of column
        worksheet.set_column(1, 11, 25)
  
    def writeHeadExcelOfSoldTransaction(self, excel, records):
        worksheet=excel.get('sheet')
        cursorPosition=excel.get('cursorPosition')
        record=records.get('record')
        format=excel.get('format')

        worksheet.write(cursorPosition,0,records.get('index'),format)
        worksheet.write(cursorPosition,1, record.th_id,format)
        worksheet.write(cursorPosition,2, record.th_date.strftime('%d/%m/%Y'),format)
        worksheet.write(cursorPosition,3, record.employee_transaction.mse_name,format)
        worksheet.write(cursorPosition,4, record.th_total_price,format)
        worksheet.write(cursorPosition,5, record.th_tax,format)
        worksheet.write(cursorPosition,6, record.th_paid,format)
        worksheet.write(cursorPosition,7, record.th_change,format)
    
    def writeDetailExcelOfSoldTransaction(self,excel,records):
        worksheet=excel.get('worksheet')
        cursorPosition=excel.get('cursorPosition')
        detail=records.get('record')
        format=excel.get('format')
        
        worksheet.write(cursorPosition, 8,detail.product.msp_id,format)
        worksheet.write(cursorPosition, 9,detail.product.msp_desc,format)
        worksheet.write(cursorPosition, 10,detail.td_quantity,format)
        worksheet.write(cursorPosition, 11,detail.td_on_sale_price,format)
    
    def writeDiscountAppliedOnSoldTransaction(self,excel,records):
        worksheet=excel.get('worksheet')
        cursorPosition=excel.get('cursorPosition')
        discount=records.get('record')
        format=excel.get('format')
        discountId,discountName="",""

        if discount.discount_applied:
            discountId= discount.discount_applied.discount_master.msd_id
            discountName= discount.discount_applied.discount_master.msd_desc

        worksheet.write(cursorPosition, 12,discount.tdda_cutt_off_nominal,format)
        worksheet.write(cursorPosition, 13,discountId,format)
        worksheet.write(cursorPosition, 14,discountName,format)

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
        

    def writeEmptyCellSoldDetail(self,excel):
        worksheet=excel.get('worksheet')
        cursorPosition=excel.get('cursorPosition')
        format=excel.get('format')

        for column in range(8,12):
            worksheet.write(cursorPosition, column, '',format)
            
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

    def writeHeaderForExcelSold(self,excel,cursorPosition):
        worksheet=excel.get('sheet')
        format=excel.get('format')
        headerExcelOfPurchasedReport=[
        'No','Transaction ID','Sold Date',
        'Cashier', 'Total Price To Paid','Tax','Paid', 
        'Change', 'Product ID', 'Product', 'Quantity', 'Price', 
        'Cutt Off', 'Discount ID', 'Discount'
        ]
        worksheet.write_row(cursorPosition, 0,headerExcelOfPurchasedReport, format.get('headFormat'))
        worksheet.set_row(cursorPosition, 35)

    def writeSoldExcelTitle(self,excel,cursorPosition):
        worksheet=excel.get('sheet')
        format=excel.get('format')
        title=[
            "Transaction Of Sold Product",
            "Generated on : "+datetime.now().strftime('%d/%m/%Y %H:%M')
        ]
        worksheet.write_column(cursorPosition, 0,title, format.get('titleFormat'))

    def writeEmptyCell(self,excel):
        worksheet=excel.get('worksheet')
        cursorPosition=excel.get('cursorPosition')
        format=excel.get('format')
        for column in range(5):
            worksheet.write(cursorPosition+1, column, '',format)

    def writeEmptyCellSold(self,excel):
        worksheet=excel.get('worksheet')
        cursorPosition=excel.get('cursorPosition')
        format=excel.get('format')
        for column in range(8):
            worksheet.write(cursorPosition+1, column, '',format)

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
