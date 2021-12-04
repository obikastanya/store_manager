import pytest
import requests 

host='http://127.0.0.1:8887'
# to run test case, run comand pytest
# to run and showing print comand, run pytest -s

# select case
@pytest.mark.selectSuccess
def testSelectCategoryProduct():
    """Check if process of selecting data is success"""
    response=requests.get(host+'/category_product_api')
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

# failed insert case
@pytest.mark.insertFailed
def testEmptyParameter():
    payload={'category':''}
    response=requests.post(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.insertFailed
def testMaxLength():
    payload={'category':"""Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Dolorem commodi facere voluptatem earum dolor alias debitis laborum iste error adipisci? 
    Vitae deleniti natus dignissimos illo Vitae deleniti natus dignissimos illo."""
                }
    response=requests.post(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.insertFailed
def testMinLength():
    payload={'category':'L'}
    response=requests.post(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

# success insert case
@pytest.mark.insertSuccess
def testMinLength():
    payload={'category':'Category From Pytest'}
    response=requests.post(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

#failed update case
@pytest.mark.updateFailed
def testEmptyCategoryId():
    payload={'category':'this is new value', 'category_id':'', 'active_status':'Y'}
    response=requests.put(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.updateFailed
def testEmptyActiveStatus():
    payload={'category':'this is new value', 'category_id':'66', 'active_status':''}
    response=requests.put(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False


@pytest.mark.updateFailed
def testEmptyParameterOnUpdate():
    payload={'category':'', 'category_id':'66', 'active_status':'Y'}
    response=requests.put(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.updateFailed
def testMaxLengthOnUpdate():
    payload={'category':"""Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Dolorem commodi facere voluptatem earum dolor alias debitis laborum iste error adipisci? 
    Vitae deleniti natus dignissimos illo Vitae deleniti natus dignissimos illo.""",'category_id':'66', 'active_status':'Y' 
                }
    response=requests.put(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.updateFailed
def testMinLengthOnUpdate():
    payload={'category':'L', 'category_id':'66', 'active_status':'Y'}
    response=requests.put(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.updateSuccess
def testSuccessOnUpdate():
    payload={'category':'this is new value', 'category_id':'66', 'active_status':'Y'}
    response=requests.put(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

# select single data case
@pytest.mark.selectSingleSuccess
def testCategoryOnSelectSingle():
    payload={'category_id':'66'}
    response=requests.get(host+'/category_product_api_search', json=payload)
    jsonResponse=response.json()
    validResponse=jsonResponse.get('status')==True and bool(len(jsonResponse.get('data'))>0)
    assert validResponse==True

@pytest.mark.selectSingleFailed
def testNotFoundCategoryOnSelectSingle():
    payload={'category_id':'000'}
    response=requests.get(host+'/category_product_api_search', json=payload)
    jsonResponse=response.json()
    validResponse=jsonResponse.get('status')==False and bool(len(jsonResponse.get('data'))<1)
    assert validResponse==True

@pytest.mark.selectSingleFailed
def testEmptyCategoryOnSelectSingle():
    payload={'category_id':''}
    response=requests.get(host+'/category_product_api_search', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.deleteFailed
def testEmptyCategoryOnDelete():
    payload={'category_id':''}
    response=requests.delete(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

@pytest.mark.deleteSuccess
def testCategoryOnDelete():
    payload={'category_id':'65'}
    response=requests.delete(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

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
    response=requests.get(host+'/category_product_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

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
    response=requests.get(host+'/category_product_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.datatableSelect
def testSelectAndOrder():
    payload={
            'search[value]':'',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'category_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/category_product_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True

@pytest.mark.datatableSelect
def testSelectWithKeywordAndOrder():
    payload={
            'search[value]':'B',
            'order[0][dir]':'asc',
            'order[0][column]':'1',
            'columns[1]][name]':'category_id',
            'start':0,
            'length':10
        }
    response=requests.get(host+'/category_product_api', params=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True


