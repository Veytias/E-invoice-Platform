import requests
from src.app import config

BASE_URL =  config.url

'''
invoice_upload server testing function
'''

'''
test 1: Unknown Report
'''

def test_upload_invoice_unknown_report():
    
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
            'report_type':("txt")}
    upload_resp = requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file,data = data)
    assert upload_resp.status_code == 400

'''
test 2: None XML file
'''

def test_upload_non_xml_file():

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")


    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    payload = register_resp.json()

    upload_file = {'file': (open('tests/test_files/AU invoice.txt','r'))}
    data = {'token': (payload),
            'report_type':("html")}
    upload_resp = requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file,data = data)
    assert upload_resp.status_code == 400

'''
test 3: Test invoice upload success
'''

def test_upload_invoice_by_API_success():
    
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
    upload_resp = requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file,data = data)
    assert upload_resp.status_code == 200

'''
test 4: Test invoice upload success by two or more users.
'''

def test_upload_invoice_by_API_success2():
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")

    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    payload = register_resp.json()

    # register in server
    register_resp2 = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'testemailiowerjfesdjf@gmail.com',
        'password': '1234567898',
        'username': 'Leo'
    })
    payload2 = register_resp2.json()

    upload_file = {'file': (open('tests/test_files/AU Invoice.xml','r'))}
    data = {'token': (payload),
            'report_type':("html")}
    upload_resp1 = requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file,data = data)

    upload_file = {'file': (open('tests/test_files/AU Invoice.xml','r'))}
    data = {'token': (payload2),
            'report_type':("html")}
    upload_resp2 = requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file,data = data)

    assert upload_resp1.status_code == 200
    assert upload_resp2.status_code == 200