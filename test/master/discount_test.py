import pytest
import requests
host='http://127.0.0.1:8887'
# to run the specific file -> pytest -m datatableSelect -v ./test/master/company_test.py

@pytest.mark.discount
@pytest.mark.datatableSelect
def testSelectDiscountWithKeywordAndOrder():
    payload={
            'search[value]':'',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'discount_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/discount_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True



@pytest.mark.discount
@pytest.mark.insertSuccess
def testInsertDiscountSuccess():
    payload={'discount':'12.12', 'discount_type':1, 'nominal':10}
    response=requests.post(host+'/discount_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.discount
@pytest.mark.selectSingleSuccess
def testDiscountOnSelectSingle():
    payload={'discount_id':'2'}
    response=requests.post(host+'/discount_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.discount
@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={'discount_id':2,'discount':'12.12 update from pytest', 'discount_type':1, 'nominal':20,'active_status':'Y'}
    response=requests.put(host+'/discount_api', json=payload)
    jsonResponse=response.json()
    print(jsonResponse)
    assert jsonResponse.get('status')==True

@pytest.mark.deleteSuccess
def testCompanyOnDelete():
    payload={'discount_id':'3'}
    response=requests.delete(host+'/discount_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True