import pytest
import requests
host='http://127.0.0.1:8887'
# to run the specific file -> pytest -m datatableSelect -v ./test/master/company_test.py

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

@pytest.mark.company
@pytest.mark.datatableSelect
def testFirstLoadNoKeywordAndOrder():
    payload={
            'search[value]':'',
            'order[0][dir]':'',
            'order[0][column]':'',
            'columns[1]][name]':'',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/company_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.company
@pytest.mark.datatableSelect
def testSelectWithKeyword():
    payload={
            'search[value]':'B',
            'order[0][dir]':'',
            'order[0][column]':'',
            'columns[1]][name]':'',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/company_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.company
@pytest.mark.datatableSelect
def testSelectAndOrder():
    payload={
            'search[value]':'',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'company_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/company_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.company
@pytest.mark.datatableSelect
def testSelectWithKeywordAndOrder():
    payload={
            'search[value]':'B',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'company_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/company_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True


