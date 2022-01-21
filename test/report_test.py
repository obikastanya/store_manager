# case
# Export transaction Purchased for certain year and year,
# Export transaction Sold, for certain year and month
# Export transaction sold and purchased for certain product and category.

from itsdangerous import json
import pytest
import requests
host='http://localhost:8887'

payload={
    'date_month':2,
    'date_year':2022,
    # 'product_id':2,
    # 'category_id':3
}
@pytest.mark.reportS
def testSelectPurchasedTransaction():
    response=requests.post(host+'/report_transaction_purchased', json=payload)
    responseJson=response.json()
    assert responseJson.get('status')==True

@pytest.mark.report
def testSelectSoldTransaction():
    response=requests.post(host+'/report_transaction_sold', json=payload)
    responseJson=response.json()
    assert responseJson.get('status')==True

