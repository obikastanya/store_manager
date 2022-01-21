from flask import request
from app import app
from application.master.indexMasterController import *
from application.manage_discount.manageDiscountController import ManageDiscountController
from application.product_sold.productSoldController import ProductSoldController
from application.product_purchased.productPurchasedController import ProductPurchasedController
from application.dashboard.dashboardController import DashboardController
from application.report.reportController import ReportController

from application.auth.authController import  AuthToken

"""Contain all api for the apps"""

# Bellow is all route for master category product
authToken=AuthToken()
fourCommonMethods=['GET', 'POST', 'PUT', 'DELETE']

@app.route('/category_product_api', methods=fourCommonMethods)
@authToken.middleware
def categoryProductApi(**kwargs):
    return splitRouteByMethods(CategoryProductController)


@app.post('/category_product_api_search')
@authToken.middleware
def categoryProductApiSearch(**kwargs):
    return CategoryProductController().searchSingleData()


# Bellow is all route for master company
@app.route('/company_api', methods=fourCommonMethods)
@authToken.middleware
def companyApi(**kwargs):
    return splitRouteByMethods(CompanyController)


@app.post('/company_api_search')
@authToken.middleware
def companyApiSearch(**kwargs):
    return CompanyController().searchSingleData()


# bellow is all route for master discount
@app.route('/discount_api', methods=fourCommonMethods)
@authToken.middleware
def discountApi(**kwargs):
    return splitRouteByMethods(DiscountController)


@app.post('/discount_api_search')
@authToken.middleware
def discountApiSearch(**kwargs):
    return DiscountController().searchSingleData()




# bellow is all route for master discount
@app.route('/discount_type_api', methods=fourCommonMethods)
@authToken.middleware
def discountTypeApi(**kwargs):
    return splitRouteByMethods(DiscountTypeController)

@app.post('/discount_type_api_search')
@authToken.middleware
def discountTypeApiSearch(**kwargs):
    return DiscountController().searchSingleData()



@app.route('/employee_api', methods=fourCommonMethods)
@authToken.middleware
def employeeApi(**kwargs):
    return splitRouteByMethods(EmployeeController)

@app.post('/employee_api_search')
@authToken.middleware
def employeeApiSearch(**kwargs):
    return EmployeeController().searchSingleData()



@app.route('/payment_method_api', methods=fourCommonMethods)
@authToken.middleware
def paymentMethodApi(**kwargs):
    return splitRouteByMethods(PaymentMethodContoller)

@app.post('/payment_method_api_search')
@authToken.middleware
def paymentMethodApiSearch(**kwargs):
    return PaymentMethodContoller().searchSingleData()



@app.route('/product_api', methods=fourCommonMethods)
@authToken.middleware
def productApi(**kwargs):
    return splitRouteByMethods(ProductController)

@app.post('/product_api_search')
@authToken.middleware
def productApiSearch(**kwargs):
    return ProductController().searchSingleData()


@app.route('/employee_status_api', methods=fourCommonMethods)
@authToken.middleware
def employeeStatusApi(**kwargs):
    return splitRouteByMethods(EmployeeStatusController)

@app.post('/employee_status_api_search')
@authToken.middleware
def employeeStatusApiSearch(**kwargs):
    return EmployeeStatusController().searchSingleData()



@app.route('/stock_api', methods=fourCommonMethods)
@authToken.middleware
def stockApi(**kwargs):
    return splitRouteByMethods(StockController)

@app.post('/stock_api_search')
@authToken.middleware
def stockApiSearch(**kwargs):
    return StockController().searchSingleData()


@app.route('/supplier_api', methods=fourCommonMethods)
@authToken.middleware
def supplierApi(**kwargs):
    return splitRouteByMethods(SupplierController)

@app.post('/supplier_api_search')
@authToken.middleware
def supplierApiSearch(**kwargs):
    return SupplierController().searchSingleData()





# Lov Api End Point
@app.get('/supplier_lov_api')
@authToken.middleware
def supplierLovApi(**kwargs):
    return SupplierController().getLovData()


@app.get('/employee_status_lov_api')
@authToken.middleware
def employeeStatusLovApi(**kwargs):
    return EmployeeStatusController().getLovData()

@app.get('/employee_lov_api')
@authToken.middleware
def employeeLovApi(**kwargs):
    return EmployeeController().getLovData()

@app.get('/category_product_lov_api')
@authToken.middleware
def categoryProductLovApi(**kwargs):
    return CategoryProductController().getLovData()


@app.get('/company_lov_api')
@authToken.middleware
def companyLovApi(**kwargs):
    return CompanyController().getLovData()

@app.get('/product_lov_api')
@authToken.middleware
def productLovApi(**kwargs):
    return ProductController().getLovData()

@app.get('/discount_lov_api')
@authToken.middleware
def discountLovApi(**kwargs):
    return DiscountController().getLovData()

@app.get('/payment_method_lov_api')
@authToken.middleware
def paymentMethodLovApi(**kwargs):
    return PaymentMethodContoller().getLovData()





# api for transaction menu
# api for manageDiscount
@app.route('/manage_discount_api', methods=fourCommonMethods)
@authToken.middleware
def manageDiscountApi(**kwargs):
    return splitRouteByMethods(ManageDiscountController)


@app.post('/manage_discount_api_search')
@authToken.middleware
def manageDiscountApiSearch(**kwargs):
    return ManageDiscountController().searchSingleData()


@app.post('/product_sold_api_search')
@authToken.middleware
def productSoldApiSearch(**kwargs):
    return ProductSoldController().searchDetailTransaction()

@app.post('/product_sold_api_filter')
@authToken.middleware
def productSoldApiFilter(**kwargs):
    return ProductSoldController().filterTransaction()

@app.route('/product_sold_api', methods=['GET','POST','DELETE'])
@authToken.middleware
def productSoldApi(**kwargs):
    if request.method=='GET':
        return ProductSoldController().getData()
    if request.method=='POST':
        return ProductSoldController().insertNewTransaction()
    if request.method=='DELETE':
        return ProductSoldController().deleteTransaction()

@app.route('/product_purchased_api', methods=['GET','POST','DELETE'])
@authToken.middleware
def productPurchasedApi(**kwargs):
    if request.method=='GET':
        return ProductPurchasedController().getData()
    if request.method=='POST':
        return ProductPurchasedController().insertNewTransaction()
    if request.method=='DELETE':
        return ProductPurchasedController().deleteTransaction()

@app.post('/product_purchased_api_search')
@authToken.middleware
def productPurchasedApiSearch(**kwargs):
    return ProductPurchasedController().searchDetailTransaction()

@app.post('/dashboard_api')
@authToken.middleware
def dashboardApi(**kwargs):
    summaryType=request.json.get('summarize_type')
    controllerMethod=getControllerMethodBySummaryType(summaryType)
    return controllerMethod()

@app.post('/report_transaction_purchased')
@authToken.middleware
def reportTransactionPurchasedApi(**kwargs):
    return ReportController().exportPurchasedTransaction()

@app.post('/report_transaction_sold')
@authToken.middleware
def reportTransactionSoldApi(**kwargs):
    return ReportController().exportSoldTransaction()

def splitRouteByMethods(Controller):
    if request.method == 'POST':
        return Controller().insertNewData()
    if request.method == 'GET':
        return Controller().getData()
    if request.method == 'PUT':
        return Controller().updateData()
    if request.method == 'DELETE':
        return Controller().deleteData()

def getControllerMethodBySummaryType(summaryType):
    dashboardInstance=DashboardController()
    groupByCategory=request.json.get('group_by_category')
    if summaryType=='summarize_total':
        return dashboardInstance.getSummerizeOfTotal

    if summaryType=='purchased_vs_sold':
        if groupByCategory:
            return dashboardInstance.getSummerizeOfPurchasedVsSoldProductByCategory
        return dashboardInstance.getSummerizeOfPurchasedVsSoldProduct

    if summaryType=='sold_summary':
        if groupByCategory:
            return dashboardInstance.getSummerizeOfSoldProductByCategory
        return dashboardInstance.getSummerizeOfSoldProduct

    if summaryType=='purchased_summary':
        if groupByCategory:
            return dashboardInstance.getSummerizeOfPurchasedProductByCategory
        return dashboardInstance.getSummerizeOfPurchasedProduct

    if summaryType=='availability_store_summary':
        return dashboardInstance.getSummerizeOfStoreAvailability

    if summaryType=='availability_warehouse_summary':
        return dashboardInstance.getSummerizeOfWarehouseAvailability

    return dashboardInstance.requestIsNotRecognize

