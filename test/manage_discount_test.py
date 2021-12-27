import pytest
import requests
from datetime import date

host = 'http://127.0.0.1:8887'
endpoint = '/manage_discount_api'


# case:
# 1. Select discount applied from table discount_applied, product, discount, discount_type.
# show product code, product name, discount_name, discount_type discount_nominal.
# table condition. product code, discount_code is must be unique.
def formatDate(date):
    return date.strftime('%Y-%m-%d')


@pytest.mark.manageDiscount
def testSelectDiscountAppliedSuccesstest():
    payload = {
        'search[value]': 'Y',
        'order[0][dir]': 'asc',
        'order[0][column]': '1',
        'columns[1]][name]': 'active_status',
        'start': 0,
        'length': 10
    }
    response = requests.get(host + endpoint, params=payload)
    jsonResponse = response.json()
    assert jsonResponse.get('status') == True


@pytest.mark.manageDiscount
def testInsertDiscountAppliedSuccess():
    payload = {
        'product_id': 1,
        'discount_id': 1,
        'start_date': formatDate(date.today()),
        'expired_date': formatDate(date.today())
    }
    response = requests.post(host + endpoint, json=payload)
    jsonResponse = response.json()
    assert jsonResponse.get('status') == True


@pytest.mark.manageDiscount
def testUpdateDiscountAppliedSuccess():
    payload = {
        'product_id': 1,
        'discount_id': 1,
        'start_date': formatDate(date.today()),
        'expired_date': formatDate(date.today()),
        'active_status': 'N'
    }
    response = requests.put(host + endpoint, json=payload)
    jsonResponse = response.json()
    assert jsonResponse.get('status') == True


@pytest.mark.manageDiscount
def testDeleteDiscountAppliedSuccess():
    payload = {'product_id': 1, 'discount_id': 1}
    response = requests.delete(host + endpoint, json=payload)
    jsonResponse = response.json()
    assert jsonResponse.get('status') == True


@pytest.mark.manageDiscount
def testSearchDiscountAppliedSuccess():
    payload = {'product_id': 1, 'discount_id': 1}
    response = requests.post(host + '/manage_discount_api_search',
                             json=payload)
    jsonResponse = response.json()
    assert jsonResponse.get('status') == True
