import pytest
import requests
from datetime import date

host = 'http://127.0.0.1:8887'
endpoint = '/product_purchased_api'

# operation.
# 1. select transaction
# 2. show detail product transaction.
# 3. insert new product transaction
# filter transaction by:
#  - product
#  - date_trx
#  - supplier

def formatDate(date):
    return date.strftime('%Y-%m-%d')

@pytest.mark.productPurchased
def testSelectProductPurchasedSuccess():
    payload = {
        'search[value]': '01',
        'order[0][dir]': 'asc',
        'order[0][column]': '1',
        'columns[1]][name]': 'transaction_date',
        'start': 0,
        'length': 10,
        'product_id':2,
        'supplier_id':1,
        'transaction_date':formatDate(date.today()),
    }
    response = requests.get(host + endpoint, params=payload)
    jsonResponse = response.json()
    assert jsonResponse.get('status') == True

@pytest.mark.productPurchased
def testShowDetailTransaction():
    payload={
        'transaction_purchased_id':7
    }
    response=requests.post(host+'/product_purchased_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.productPurchased
def testInsertNewTransaction():
    payload={
        'supplier_id':1,
        'payment_method':1,
        'nominal':6000,
        'transaction_date':formatDate(date.today()),
        'product_purchased':[
            {
                'product_id':2, 'quantity':3, 'product_price':500
            },
            {
                'product_id':2, 'quantity':3, 'product_price':500
            },
        ]
    }
    response=requests.post(host+endpoint, json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

    
@pytest.mark.productSold
def testDeleteTransaction():
    payload={
        'transaction_purchased_id':2
    }
    response=requests.delete(host+endpoint, json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

