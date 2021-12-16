import pytest
import requests
host='http://127.0.0.1:8887'
# to run the specific file -> pytest -m datatableSelect -v ./test/master/product_test.py

@pytest.mark.product
@pytest.mark.datatableSelect
def testSelectProductWithKeywordAndOrder():
    payload={
            'search[value]':'a',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'product_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/product_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True



@pytest.mark.product
@pytest.mark.insertSuccess
def testInsertProductSuccess():
    payload={
        'product_desc':'Indomie rasa rendang',
        'brand':'', 
        'price':300,
        'category':1,
        'supplier':1,
        'company':2
        }
    response=requests.post(host+'/product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.product
@pytest.mark.selectSingleSuccess
def testproductOnSelectSingle():
    payload={'product_id':'1'}
    response=requests.post(host+'/product_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.product
@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={
        'product_id':1,
        'product_desc':'Indomie rasa rendang',
        'brand':'', 
        'price':300,
        'category':1,
        'supplier':1,
        'company':2,
        'active_status':'Y'
        }
    response=requests.put(host+'/product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.deleteSuccess
def testProductOnDelete():
    payload={'product_id':'1'}
    response=requests.delete(host+'/product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True