import pytest
import requests
from datetime import date
from sqlalchemy.sql.sqltypes import DateTime
host='http://127.0.0.1:8887'
# to run the specific file -> pytest -m datatableSelect -v ./test/master/company_test.py

def formatDate(date):
    return date.strftime('%Y-%m-%d')

@pytest.mark.stock
@pytest.mark.datatableSelect
def testSelectStockWithKeywordAndOrder():
    payload={
            'search[value]':'',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'product_desc',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/stock_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True



@pytest.mark.stock
@pytest.mark.insertSuccess
def testInsertStockSuccess():
    payload={
            'product_id':1,
            'store_stock':3,
            'warehouse_stock':5
        }
    response=requests.post(host+'/stock_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.stock
@pytest.mark.selectSingleSuccess
def testStockOnSelectSingle():
    payload={'stock_id':1}
    response=requests.post(host+'/stock_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.stock
@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={
            'stock_id':1,
            'product_id':1,
            'store_stock':4,
            'warehouse_stock':5
        }
    response=requests.put(host+'/stock_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.deleteSuccess
def testStockOnDelete():
    payload={'stock_id':2}
    response=requests.delete(host+'/stock_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True