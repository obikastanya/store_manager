import pytest
import requests
host='http://127.0.0.1:8887'
# to run the specific file -> pytest -m datatableSelect -v ./test/master/company_test.py

@pytest.mark.discount
@pytest.mark.datatableSelect
def testSelectDiscountTypeWithKeywordAndOrder():
    payload={
            'search[value]':'',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'discount_type_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/discount_type_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.discount
@pytest.mark.insertSuccess
def testInsertDiscountTypeSuccess():
    payload={'discount_type':'Percent'}
    response=requests.post(host+'/discount_type_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.discount
@pytest.mark.selectSingleSuccess
def testDiscountOnSelectSingle():
    payload={'discount_type_id':1}
    response=requests.post(host+'/discount_type_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.discount
@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={'discount_type_id':1,'discount_type':'Percent upd','active_status':'Y'}
    response=requests.put(host+'/discount_type_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.deleteSuccess
def testCompanyOnDelete():
    payload={'discount_type_id':1}
    response=requests.delete(host+'/discount_type_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False