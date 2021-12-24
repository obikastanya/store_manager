import pytest
import requests
from datetime import date
from sqlalchemy.sql.sqltypes import DateTime
host='http://127.0.0.1:8887'
# to run the specific file -> pytest -m datatableSelect -v ./test/master/supplier_test.py

def formatDate(date):
    return date.strftime('%Y-%m-%d')

@pytest.mark.supplier
@pytest.mark.datatableSelect
def testSelectSupplierWithKeywordAndOrder():
    payload={
            'search[value]':'s',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'supplier_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/supplier_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True


@pytest.mark.supplier
@pytest.mark.insertSuccess
def testInsertSupplierSuccess():
    payload={
            'supplier':'supplier 1',
            'phone_number':'082394387',
            'address':'Jl. Rasuna Said No.36, RT.004/RW.005, Panunggangan Utara, Kec. Pinang, Kota Tangerang, Banten 15143'
        }
    response=requests.post(host+'/supplier_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.supplier
@pytest.mark.selectSingleSuccess
def testSupplierOnSelectSingle():
    payload={'supplier_id':1}
    response=requests.post(host+'/supplier_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.supplier
@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={
            'supplier_id':1,
            'supplier':'supplier 1 update',
            'phone_number':'082394387',
            'address':'Jl. Rasuna Said No.36, RT.004/RW.005, Panunggangan Utara, Kec. Pinang, Kota Tangerang, Banten 15143',
            'active_status':'N'
        }
    response=requests.put(host+'/supplier_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.deleteSuccess
def testSupplierOnDelete():
    payload={'supplier_id':2}
    response=requests.delete(host+'/supplier_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True