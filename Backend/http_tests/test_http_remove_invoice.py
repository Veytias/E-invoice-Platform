from os import remove
import requests
import json
from src.app import config

BASE_URL = config.url

'''
report_remove server testing function
'''

'''
test1: invoice remove success
'''

def test_invoices_remove_success():
    # Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")

    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    payload = register_resp.json()

    upload_file = {'file': (open('tests/test_files/AU Invoice.xml', 'r'))}
    data = {'token': payload,
            'report_type': "html"}
    requests.post(f"{BASE_URL}/invoice/upload/API", files=upload_file, data=data)

    result = requests.delete(f"{BASE_URL}/invoices/remove", json={
        'token': payload,
        'invoice_id': 1
    })

    assert result.status_code == 200

'''
test2: invalid_invoices
'''
def test_invalid_invoices():
    # Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")

    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    payload = register_resp.json()

    upload_file = {'file': (open('tests/test_files/AU Invoice.xml', 'r'))}
    data = {'token': payload,
            'report_type': "html"}
    requests.post(f"{BASE_URL}/invoice/upload/API", files=upload_file, data=data)

    remove_invoices = requests.delete(f"{BASE_URL}/invoices/remove", json={
        'token': payload,
        'invoice_id': 3
    })

    assert remove_invoices.status_code == 500

'''
test3: invalid_token
'''
def test_invalid_token():
    # Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")

    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    payload = register_resp.json()

    register_resp2 = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331239@gmail.com',
        'password': 'z5331239',
        'username': 'King'
    })
    payload2 = register_resp2.json()

    upload_file = {'file': (open('tests/test_files/AU Invoice.xml', 'r'))}
    data = {'token': payload,
            'report_type': "html"}
    requests.post(f"{BASE_URL}/invoice/upload/API", files=upload_file, data=data)

    remove_invoices = requests.delete(f"{BASE_URL}/invoices/remove", json={
        'token': payload2 + 'abc',
        'invoice_id': 5
    })

    assert remove_invoices.status_code == 403

'''
test4: invalid_register
'''
def test_invalid_registers():
    # Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")

    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail',
        'password': 'z5331259',
        'username': 'King'
    })
    payload = register_resp.json()

    remove_invoices = requests.delete(f"{BASE_URL}/invoices/remove", json={
        'token': payload,
        'invoice_id': 3
    })

    assert remove_invoices.status_code == 403