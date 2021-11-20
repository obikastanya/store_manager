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
    print('empyt ',jsonResponse)
    assert jsonResponse.get('status')==False

@pytest.mark.insertFailed
def testMaxLength():
    payload={'category':"""Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Dolorem commodi facere voluptatem earum dolor alias debitis laborum iste error adipisci? 
    Vitae deleniti natus dignissimos illo Vitae deleniti natus dignissimos illo."""
                }
    response=requests.post(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    print('maxLength ',jsonResponse)
    assert jsonResponse.get('status')==False

@pytest.mark.insertFailed
def testMinLength():
    payload={'category':'L'}
    response=requests.post(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==False

# success insert case
@pytest.mark.insertSuccessActive
def testMinLength():
    payload={'category':'Category From Pytest'}
    response=requests.post(host+'/category_product_api', json=payload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True
