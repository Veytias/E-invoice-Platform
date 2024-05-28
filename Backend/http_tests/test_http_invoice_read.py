import requests
from src.app import config

BASE_URL =  config.url

'''
report_lsit server testing function
'''

'''
test1: report read add success
'''

def test_invoices_read_success():
    
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

    result = requests.get(f"{BASE_URL}/invoices/read?token={payload}&invoice_id={1}")

    assert result.status_code == 200