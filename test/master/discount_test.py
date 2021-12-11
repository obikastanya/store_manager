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


