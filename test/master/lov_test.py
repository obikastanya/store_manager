import pytest
import requests
host='http://127.0.0.1:8887'

@pytest.mark.lov
@pytest.mark.supplier
def testSelectLovSupplier():
    response=requests.get(host+'/supplier_lov_api')
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True


@pytest.mark.lov
@pytest.mark.discountType
def testSelectLovDiscountType():
    response=requests.get(host+'/employee_status_lov_api')
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True


@pytest.mark.lov
@pytest.mark.categoryProduct
def testSelectLovCategoryProduct():
    response=requests.get(host+'/category_product_lov_api')
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True


@pytest.mark.lov
@pytest.mark.company
def testSelectLovCompany():
    response=requests.get(host+'/company_lov_api')
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True