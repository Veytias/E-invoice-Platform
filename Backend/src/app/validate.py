# validation API not working hence we simulate validation behavior
import random

import requests


def validate_invoice1(path):
    #default message
    message = "External Validation API Error"
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJncm91cF9pZCI6OX0.pVnMjQXI99Xp159k13jdaqlMs2Uv-vekUwQ4Mk_1SXY"
    types = 'json'
    file = (open(path, 'r'))
    upload_file = {'invoice': file}
    data = {'token': token,
            'rules': 1,
            'output_type': types}
    upload_resp = requests.post(f"http://invoicevalidation.services:8080/verify_invoice", files=upload_file, data=data)

    if upload_resp.status_code == 200:
        message = upload_resp.json()['message']

    #use backup api
    else:
        random_number = random.randint(10, 100)
        random_email = str(random_number) + '@gmail.com'
        result = requests.post("https://go-apple-pie.herokuapp.com/auth/register", json={
            'email': random_email,
            'password': 'z5331259!',
            "name_first": "12345678!fds1",
            "name_last": "12345678!fds1"
        })

        if result.status_code == 200:
            token2 = result.json()['token']
            validate_upload = "https://go-apple-pie.herokuapp.com/invoice/validate" + "?token=" + token2
            with open(path, 'rb') as xml:
                upload_resp2 = requests.post(validate_upload, data=xml)

            if upload_resp2.status_code == 200:
                message = upload_resp2.json()['message']
                
    return message

# backup API
def validate_invoice2(path):
    random_number = random.randint(10, 100)
    random_email = str(random_number) + '@gmail.com'
    result = requests.post("https://go-apple-pie.herokuapp.com/auth/register", json={
        'email': random_email,
        'password': 'z5331259!',
        "name_first": "12345678!fds1",
        "name_last": "12345678!fds1"
    })
    token2 = result.json()['token']
     
    validate_upload = "https://go-apple-pie.herokuapp.com/invoice/validate" + "?token=" + token2
    # print(validate_upload)

    with open(path, 'rb') as xml:
        upload_resp2 = requests.post(validate_upload, data=xml)

    message2 = upload_resp2.json()['message']

    if upload_resp2.status_code == 200:
        return message2
    else:
        return "error"
