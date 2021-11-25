import pytest
import requests
host='http://127.0.0.1:8887'

@pytest.mark.company
@pytest.mark.selectCompanyFailed
def testSelectCompanyEmptyOffset():
    payload={'start':'', 'length':10}
    rawResponse=requests.get(host+'/company_api', params=payload)
    jsonResponse=rawResponse.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.selectCompanyFailed
def testSelectCompanyEmptyLimit():
    payload={'start':0, 'length':''}
    rawResponse=requests.get(host+'/company_api',params=payload)
    jsonResponse=rawResponse.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.selectCompanyFailed
def testSelectCompanyEmptyOffsetLimit():
    payload={'start':'', 'length':''}
    rawResponse=requests.get(host+'/company_api', params=payload)
    jsonResponse=rawResponse.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.selectCompanySuccess
def testSelectCompanySuccess():
    payload={'start':0, 'length':10}
    rawResponse=requests.get(host+'/company_api',params=payload)
    jsonResponse=rawResponse.json()
    assert jsonResponse.get('status')==True