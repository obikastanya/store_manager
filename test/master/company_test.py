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


@pytest.mark.company
@pytest.mark.insertFailed
def testEmptyCompany():
    payload={
            'company':'',
        }
    response=requests.post(host+'/company_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False


@pytest.mark.company
@pytest.mark.insertFailed
def testEmptyCompany():
    payload={
            'company':'',
        }
    response=requests.post(host+'/company_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.insertFailed
def testMaxLength():
    payload={'company':"""Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Dolorem commodi facere voluptatem earum dolor alias debitis laborum iste error adipisci? 
    Vitae deleniti natus dignissimos illo Vitae deleniti natus dignissimos illo."""
                }
    response=requests.post(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.insertFailed
def testMinLength():
    payload={'company':'L'}
    response=requests.post(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.insertSuccess
def testInsertSuccess():
    payload={'company':'Company From Pytest'}
    response=requests.post(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

# select single data
@pytest.mark.company
@pytest.mark.selectSingleSuccess
def testCompanyOnSelectSingle():
    payload={'company_id':'2'}
    response=requests.post(host+'/company_api_search', json=payload)
    jsonResponse=response.json()
    validResponse=jsonResponse.get('status')==True and bool(len(jsonResponse.get('data'))>0)
    assert validResponse==True

@pytest.mark.company
@pytest.mark.selectSingleFailed
def testNotFoundCompanyOnSelectSingle():
    payload={'company_id':'000'}
    response=requests.post(host+'/company_api_search', json=payload)
    jsonResponse=response.json()
    validResponse=jsonResponse.get('status')==False and bool(len(jsonResponse.get('data'))<1)
    assert validResponse==True

@pytest.mark.company
@pytest.mark.selectSingleFailed
def testEmptyCompanyOnSelectSingle():
    payload={'company_id':''}
    response=requests.post(host+'/company_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

#failed update case
@pytest.mark.company
@pytest.mark.updateFailed
def testEmptyCompanyId():
    payload={'company':'this is new value', 'company_id':'', 'active_status':'Y'}
    response=requests.put(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.updateFailed
def testEmptyActiveStatus():
    payload={'company':'this is new value', 'company_id':'2', 'active_status':''}
    response=requests.put(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.updateFailed
def testEmptyParameterOnUpdate():
    payload={'company':'', 'company_id':'2', 'active_status':'Y'}
    response=requests.put(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.updateFailed
def testMaxLengthOnUpdate():
    payload={'company':"""Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Dolorem commodi facere voluptatem earum dolor alias debitis laborum iste error adipisci? 
    Vitae deleniti natus dignissimos illo Vitae deleniti natus dignissimos illo.""",'company_id':'2', 'active_status':'Y' 
                }
    response=requests.put(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.updateFailed
def testMinLengthOnUpdate():
    payload={'company':'L', 'company_id':'2', 'active_status':'Y'}
    response=requests.put(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.company
@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={'company':'this is new value', 'company_id':'2', 'active_status':'Y'}
    response=requests.put(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

# delete records
@pytest.mark.deleteFailed
def testEmptyCompanyOnDelete():
    payload={'company_id':''}
    response=requests.delete(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

# need to change the id to existing id before run the test
@pytest.mark.deleteSuccess
def testCompanyOnDelete():
    payload={'company_id':'3'}
    response=requests.delete(host+'/company_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True
