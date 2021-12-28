import pytest
import requests
from datetime import date

host = 'http://127.0.0.1:8887'
endpoint = '/product_sold_api'

# operation.
# 1. select transaction
# 2. show detail product transaction.
# 3. insert new product transaction
# filter transaction by:
#  - product
#  - discount
#  - date_trx
#  - cashier

def formatDate(date):
    return date.strftime('%Y-%m-%d')

@pytest.mark.productSold
def testSelectProductSoldSuccess():
    payload = {
        'search[value]': '01',
        'order[0][dir]': 'asc',
        'order[0][column]': '1',
        'columns[1]][name]': 'transaction_date',
        'start': 0,
        'length': 10
    }
    response = requests.get(host + endpoint, params=payload)
    jsonResponse = response.json()
    assert jsonResponse.get('status') == True

@pytest.mark.productSold
def testShowDetailTransaction():
    payload={
        'transaction_id':1
    }
    response=requests.post(host+'/product_sold_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.productSold
def testInsertNewTransaction():
    payload={
        'cashier_id':1,
        'payment_method':1,
        'paid':2000,
        'product_sold':[
            {
                'product_id':1, 'qty':3, 'product_price':500,
                'discount_applied':[
                    {
                        'discount_id':1,
                        'discount_type_id':1,
                        'cut_off_nominal':200
                    },
                    {
                        'discount_id':2,
                        'discount_type_id':1,
                        'cut_off_nominal':150
                    }
                ]
            },
            {
                'product_id':2, 'qty':3, 'product_price':500,
                'discount_applied':[]
            },
        ]
    }
    response=requests.post(host+'/product_sold_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.productSold
def testFilterTransaction():
    payload={
        'product_id':1,
        'discount_id':1,
        'cashier_id':1,
        'transaction_date':formatDate(date.today())
    }
    response=requests.post(host+'/product_sold_api_filter', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.productSold
def testDeleteTransaction():
    payload={
        'transaction_id':1
    }
    response=requests.delete(host+'/product_sold_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

