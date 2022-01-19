import pytest
import requests
from datetime import date
import copy

host = 'http://127.0.0.1:8887'
endpoint = '/dashboard_api'

# test case:
# - Select on first load. 
        # - select for badge including 
        #   - total cash in from transaction sales
        #   - total Cash Out from purchasing 
        #   - Total Transaction head of Product Sold
        #   - Total Transaction head of product Purchased
        #   - Total Product inside Master Stock, summary from warehouse and store stock.
        # - Select For Purchasing vs Sold Group statistic. 
        #   Summerize the total price to be paid and summerize the nominal purchasing.
        #   Group them by month or date depends on parameter send.
# - Select Product Sold. Select total transaction sold and group them by date or month. 
# - Select Product Sold. Select total transaction sold and group them by date or month and group them with specific category. 
# - Select Purchased is the same as Sold.
# - select Availability. Select total store stock and select total warehouse stock. 

payload={
    'date_month':'1',
    'date_year':'2022',
    'summarize_type':'',
    'group_by_category':''
}

# Test case
# succeed
@pytest.mark.dashboardTest
def testSelectDataForBadge():
    # expected result 
    # result={
    #     'total_cash_in':0,
    #     'total_cash_out':0,
    #     'total_transaction_product_sold':0,
    #     'total_transaction_product_purchased':0,
    #     'total_product_in_store':0
    #     }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'summarize_total'})
    return runTest(currentPayload)
    

@pytest.mark.dashboardTest
def testSelectPurchasedVsSoldGroupByMonth():
    # expected result
    # result={
    #     'januari':20,
    #     'februari':30,
    #     'sept':30,
    #     # ...
    # }
    # and 
    # result={
    #     '1':20,
    #     '2':30,
    #     '3':30,
    #     # ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'purchased_vs_sold','date_month':''})
    return runTest(currentPayload)

@pytest.mark.dashboardTest
def testSelectPurchasedVsSoldGroupByDate():
    # expected result
    # result={
    #     'januari':20,
    #     'februari':30,
    #     'sept':30,
    #     # ...
    # }
    # and 
    # result={
    #     '1':20,
    #     '2':30,
    #     '3':30,
    #     # ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'purchased_vs_sold'})
    return runTest(currentPayload)

@pytest.mark.dashboardTest
def testSelectPurchasedVsSoldGroupByCategory():
    # expected result
    # result={
    #     'cosmetic':20,
    #     'food':30,
    #       ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'purchased_vs_sold', 'group_by_category':True})
    return runTest(currentPayload)



@pytest.mark.dashboardTest
def testSelectSoldGroupByDate():
    # expected result
    # result={
    #     'januari':20,
    #     'februari':30,
    #     'sept':30,
    #     # ...
    # }
    # and 
    # result={
    #     '1':20,
    #     '2':30,
    #     '3':30,
    #     # ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'sold_summary'})
    return runTest(currentPayload)


@pytest.mark.dashboardTest
def testSelectSoldGroupByMonth():
    # expected result
    # result={
    #     'januari':20,
    #     'februari':30,
    #     'sept':30,
    #     # ...
    # }
    # and 
    # result={
    #     '1':20,
    #     '2':30,
    #     '3':30,
    #     # ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'sold_summary', 'date_month':''})
    return runTest(currentPayload)

@pytest.mark.dashboardTest
def testSelectSoldGroupByCategory():
    # expected result
    # result={
    #     'cosmetic':20,
    #     'food':30,
    #       ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'sold_summary', 'group_by_category':True})
    return runTest(currentPayload)

# wip
@pytest.mark.dashboardTest
def testSelectPurchasedGroupByDate():
    # expected result
    # result={
    #     'januari':20,
    #     'februari':30,
    #     'sept':30,
    #     # ...
    # }
    # and 
    # result={
    #     '1':20,
    #     '2':30,
    #     '3':30,
    #     # ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'purchased_summary'})
    return runTest(currentPayload)

@pytest.mark.dashboardTest
def testSelectPurchasedGroupByMonth():
    # expected result
    # result={
    #     'januari':20,
    #     'februari':30,
    #     'sept':30,
    #     # ...
    # }
    # and 
    # result={
    #     '1':20,
    #     '2':30,
    #     '3':30,
    #     # ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'purchased_summary','date_month':''})
    return runTest(currentPayload)

@pytest.mark.dashboardTest
def testSelectPurchasedGroupByCategory():
    # expected result
    # result={
    #     'cosmetic':20,
    #     'food':30,
    #       ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'purchased_summary', 'group_by_category':True})
    return runTest(currentPayload)


@pytest.mark.dashboardTest
def testSelectAvailabiityStoreGroupByCategory():
    # expected result
    # result={
    #     'cosmetic':20,
    #     'food':30,
    #       ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'availability_store_summary'})
    return runTest(currentPayload)

@pytest.mark.dashboardTest
def testSelectAvailabiityWarehouseByCategory():
    # expected result
    # result={
    #     'cosmetic':20,
    #     'food':30,
    #       ...
    # }
    currentPayload=payload.copy()
    currentPayload.update({'summarize_type':'availability_warehouse_summary'})
    return runTest(currentPayload)

def runTest(testPayload):
    response=requests.post(host+endpoint, json=testPayload)
    jsonResponse=response.json()
    assert jsonResponse.get('status')==True
    