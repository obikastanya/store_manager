import pytest
import requests
host='http://127.0.0.1:8887'
# to run the specific file -> pytest -m datatableSelect -v ./test/master/employe_status_test.py

@pytest.mark.employeStatus
@pytest.mark.datatableSelect
def testSelectEmployeStatusWithKeywordAndOrder():
    payload={
            'search[value]':'a',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'employee_status_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/employee_status_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True



@pytest.mark.employeStatus
@pytest.mark.insertSuccess
def testInsertEmployeStatusSuccess():
    payload={
        'employee_status':'Cuti'
        }
    response=requests.post(host+'/employee_status_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.employeStatus
@pytest.mark.selectSingleSuccess
def testEmployeStatusOnSelectSingle():
    payload={'employee_status_id':'1'}
    response=requests.post(host+'/employee_status_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.employeStatus
@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={
        'employee_status_id':1,
        'employee_status':'Cuti update',
        'active_status':'Y'
        }
    response=requests.put(host+'/employee_status_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.employeStatus
@pytest.mark.deleteSuccess
def testEmployeStatusOnDelete():
    payload={'employee_status_id':'1'}
    response=requests.delete(host+'/employee_status_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True