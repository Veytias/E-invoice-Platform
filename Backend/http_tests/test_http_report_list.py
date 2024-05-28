import requests
import json
from src.app import config

BASE_URL =  config.url

'''
report_lsit server testing function
'''

'''
test1: report list add success
'''

def test_reports_list_success():
    
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
    

    result = requests.get(f"{BASE_URL}/reports/list?token={payload}")

    assert result.status_code == 200

def test_more_reports_get_in_list():
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")

    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    payload = register_resp.json()

    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'username': 'Leo'
    })
    payload2 = register_resp.json()

    upload_file = {'file': (open('tests/test_files/AU Invoice.xml','r'))}
    data = {'token': (payload),
            'report_type':("html")}
    requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file,data = data)
    
    upload_file2 = {'file': (open('tests/test_files/AU Invoice.xml','r'))}
    data2 = {'token': (payload2),
            'report_type':("html")}
    requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file2,data = data2)

    result = requests.get(f"{BASE_URL}/reports/list?token={payload}")

    assert result.status_code == 200