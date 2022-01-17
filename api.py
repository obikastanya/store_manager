from flask import request, abort
from app import app
from application.master.indexMasterController import *
from application.manage_discount.manageDiscountController import ManageDiscountController
from application.product_sold.productSoldController import ProductSoldController
from application.product_purchased.productPurchasedController import ProductPurchasedController
from application.dashboard.dashboardController import DashboardController


"""Contain all api for the apps"""

# Bellow is all route for master category product
@app.route('/category_product_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def categoryProductApi():
    return splitRouteByMethods(CategoryProductController)


@app.post('/category_product_api_search')
def categoryProductApiSearch():
    return CategoryProductController().searchSingleData()


# Bellow is all route for master company
@app.route('/company_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def companyApi():
    return splitRouteByMethods(CompanyController)


@app.post('/company_api_search')
def companyApiSearch():
    return CompanyController().searchSingleData()


# bellow is all route for master discount
@app.route('/discount_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def discountApi():
    return splitRouteByMethods(DiscountController)


@app.post('/discount_api_search')
def discountApiSearch():
    return DiscountController().searchSingleData()




# bellow is all route for master discount
@app.route('/discount_type_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def discountTypeApi():
    return splitRouteByMethods(DiscountTypeController)

@app.post('/discount_type_api_search')
def discountTypeApiSearch():
    return DiscountController().searchSingleData()



@app.route('/employee_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def employeeApi():
    return splitRouteByMethods(EmployeeController)

@app.post('/employee_api_search')
def employeeApiSearch():
    return EmployeeController().searchSingleData()




@app.route('/payment_method_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def paymentMethodApi():
    return splitRouteByMethods(PaymentMethodContoller)

@app.post('/payment_method_api_search')
def paymentMethodApiSearch():
    return PaymentMethodContoller().searchSingleData()



@app.route('/product_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def productApi():
    return splitRouteByMethods(ProductController)

@app.post('/product_api_search')
def productApiSearch():
    return ProductController().searchSingleData()



@app.route('/employee_status_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def employeeStatusApi():
    return splitRouteByMethods(EmployeeStatusController)

@app.post('/employee_status_api_search')
def employeeStatusApiSearch():
    return EmployeeStatusController().searchSingleData()



@app.route('/stock_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def stockApi():
    return splitRouteByMethods(StockController)

@app.post('/stock_api_search')
def stockApiSearch():
    return StockController().searchSingleData()


@app.route('/supplier_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def supplierApi():
    return splitRouteByMethods(SupplierController)

@app.post('/supplier_api_search')
def supplierApiSearch():
    return SupplierController().searchSingleData()





# Lov Api End Point
@app.get('/supplier_lov_api')
def supplierLovApi():
    return SupplierController().getLovData()


@app.get('/employee_status_lov_api')
def employeeStatusLovApi():
    return EmployeeStatusController().getLovData()

@app.get('/employee_lov_api')
def employeeLovApi():
    return EmployeeController().getLovData()

@app.get('/category_product_lov_api')
def categoryProductLovApi():
    return CategoryProductController().getLovData()


@app.get('/company_lov_api')
def companyLovApi():
    return CompanyController().getLovData()

@app.get('/product_lov_api')
def productLovApi():
    return ProductController().getLovData()

@app.get('/discount_lov_api')
def discountLovApi():
    return DiscountController().getLovData()

@app.get('/payment_method_lov_api')
def paymentMethodLovApi():
    return PaymentMethodContoller().getLovData()





# api for transaction menu
# api for manageDiscount
@app.route('/manage_discount_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manageDiscountApi():
    return splitRouteByMethods(ManageDiscountController)


@app.post('/manage_discount_api_search')
def manageDiscountApiSearch():
    return ManageDiscountController().searchSingleData()


@app.post('/product_sold_api_search')
def productSoldApiSearch():
    return ProductSoldController().searchDetailTransaction()

@app.post('/product_sold_api_filter')
def productSoldApiFilter():
    return ProductSoldController().filterTransaction()

@app.route('/product_sold_api', methods=['GET','POST','DELETE'])
def productSoldApi():
    if request.method=='GET':
        return ProductSoldController().getData()
    if request.method=='POST':
        return ProductSoldController().insertNewTransaction()
    if request.method=='DELETE':
        return ProductSoldController().deleteTransaction()

@app.route('/product_purchased_api', methods=['GET','POST','DELETE'])
def productPurchasedApi():
    if request.method=='GET':
        return ProductPurchasedController().getData()
    if request.method=='POST':
        return ProductPurchasedController().insertNewTransaction()
    if request.method=='DELETE':
        return ProductPurchasedController().deleteTransaction()

@app.post('/product_purchased_api_search')
def productPurchasedApiSearch():
    return ProductPurchasedController().searchDetailTransaction()

@app.get('/dashboard_api')
def dashboardApi():
    summaryType=request.args.get('summarize_type')
    controllerMethod=getControllerMethodBySummaryType(summaryType)
    return controllerMethod()




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
    if summaryType=='summarize_total':
        return dashboardInstance.getSummerizeOfTotal

    if summaryType=='purchased_vs_sold':
        if request.args.get('group_by_category'):
            return dashboardInstance.getSummerizeOfPurchasedVsSoldProductByCategory
        return dashboardInstance.getSummerizeOfPurchasedVsSoldProduct

    if summaryType=='sold_summary':
        return dashboardInstance.getSummerizeOfSoldTransaction

    if summaryType=='purchased_summary':
        return dashboardInstance.getSummerizeOfPurchasedTransaction

    if summaryType=='availability_store_summary':
        return dashboardInstance.getSummerizeOfStoreAvailability

    if summaryType=='availability_warehouse_summary':
        return dashboardInstance.getSummerizeOfWarehouseAvailability
        
    return dashboardInstance.requestIsNotRecognize

