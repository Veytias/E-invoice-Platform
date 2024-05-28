import requests
from src.app import config

BASE_URL =  config.url

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
    requests.post(f"{BASE_URL}/invoice/upload/API", files= upload_file,data = data)
    send_resp = requests.post(f"{BASE_URL}/invoice/send", json={
        'token': payload,
        'invoice_id': 1,
        'recipientEmail': "barry649613419@gmail.com"
    })
    assert send_resp.status_code == 200