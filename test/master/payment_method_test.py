import pytest
import requests
host='http://127.0.0.1:8887'
# to run the specific file -> pytest -m datatableSelect -v ./test/master/payment_method_test.py


@pytest.mark.paymentMethod
@pytest.mark.datatableSelect
def testSelectpayment_methodWithKeywordAndOrder():
    payload={
            'search[value]':'a',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'payment_method_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/payment_method_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True



@pytest.mark.paymentMethod
@pytest.mark.insertSuccess
def testInsertpaymentMethodSuccess():
    payload={
            'payment_method':'Debit from pytest',
        }
    response=requests.post(host+'/payment_method_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.paymentMethod
@pytest.mark.selectSingleSuccess
def testpaymentMethodOnSelectSingle():
    payload={'payment_method_id':1}
    response=requests.post(host+'/payment_method_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.paymentMethod
@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={
            'payment_method_id':1,
            'payment_method':'Debit updated from pytest',
            'active_status':'N'
            }
    response=requests.put(host+'/payment_method_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.paymentMethod
@pytest.mark.deleteSuccess
def testpaymentMethodOnDelete():
    payload={'payment_method_id':1}
    response=requests.delete(host+'/payment_method_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True