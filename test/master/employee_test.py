import pytest
import requests
from datetime import date
from sqlalchemy.sql.sqltypes import DateTime
host='http://127.0.0.1:8887'
# to run the specific file -> pytest -m datatableSelect -v ./test/master/company_test.py

def formatDate(date):
    return date.strftime('%Y-%m-%d')

@pytest.mark.employee
@pytest.mark.datatableSelect
def testSelectEmployeeWithKeywordAndOrder():
    payload={
            'search[value]':'',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'employee_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/employee_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True



@pytest.mark.employee
@pytest.mark.insertSuccess
def testInsertEmployeeSuccess():
    payload={
            'employee_status_id':1,
            'name':'Obi Kastanya',
            'phone_number':'081209092345',
            'email':'obikastanya@gmail.com',
            'address':'Jl. Rasuna Said No.36, RT.004/RW.005, Panunggangan Utara, Kec. Pinang, Kota Tangerang, Banten 15143',
            'salary':900,
            'position':'Crew',
            'start_working': formatDate(date.today()),
            'end_working':formatDate(date.today())
        }
    response=requests.post(host+'/employee_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.employee
@pytest.mark.selectSingleSuccess
def testEmployeeOnSelectSingle():
    payload={'employee_id':1}
    response=requests.post(host+'/employee_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.employee
@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={
            'employee_id':1,
            'employee_status_id':1,
            'name':'Obi Kastanya',
            'phone_number':'081209092345',
            'email':'obikastanya@gmail.com',
            'address':'Jl. Rasuna Said No.36, RT.004/RW.005, Panunggangan Utara, Kec. Pinang, Kota Tangerang, Banten 15143',
            'salary':900,
            'position':'Crew',
            'start_working':formatDate(date.today()),
            'end_working':formatDate(date.today())
            }
    response=requests.put(host+'/employee_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.deleteSuccess
def testEmployeeOnDelete():
    payload={'employee_id':1}
    response=requests.delete(host+'/employee_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True