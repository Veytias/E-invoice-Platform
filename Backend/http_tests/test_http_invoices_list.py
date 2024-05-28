import requests
import json
from src.app import config

BASE_URL =  config.url

'''
invoices_lsit server testing function
'''

'''
test1: invoice list add success.
'''

def test_invoices_list_success():
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")

    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })

    payload = register_resp.json()

    upload_file = {'file': (open('tests/test_files/AU Invoice.xml','r'))}
    data = {'token': (payload),
            'report_type':("html")}
    requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file,data = data)
    
    result = requests.get(f"{BASE_URL}/invoices/list?token={payload}")

    assert result.status_code == 200

'''
test2: invoice list add one more success.
'''

def test_invoices_list_second_success():
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")

    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'testemail@gmail.com',
        'password': '123465',
        'username': 'Leo'
    })
    payload = register_resp.json()

    upload_file = {'file': (open('tests/test_files/AU Invoice.xml','r'))}
    data = {'token': (payload),
            'report_type':("html")}
    requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file,data = data)

    result = requests.get(f"{BASE_URL}/invoices/list?token={payload}")

    assert result.status_code == 200
