import requests
import json
import os
from src.app import error
from src.app import invoice
from src.app import helper

def create_invoice(token,json_file):
    helper.check_token(token)
    json_file = json.loads(json_file.read())
    result = requests.post("http://seng-donut-frontend.azurewebsites.net/json/convert", json = json_file)
    if result.status_code != 200:
        raise error.ExternalAPIError(description="Creation failure")
    with open("invoices/invoice.xml",'wb') as TmpFIle:
        TmpFIle.write(result.content)
    with open("invoices/invoice.xml",'r') as File:
        result = invoice.invoice_upload_API(token, File, "html")
    helper.delFileByPath("invoices/invoice.xml")
    return result

def create_invoice_v2(token, filename, json_file):
    helper.check_token(token)
    json_file = json.loads(json_file.read())
    result = requests.post("http://seng-donut-frontend.azurewebsites.net/json/convert", json = json_file)
    if result.status_code != 200:
        raise error.ExternalAPIError(description="Creation failure")
    with open(f"invoices/{filename}.xml",'wb') as TmpFIle:
        TmpFIle.write(result.content)
    with open(f"invoices/{filename}.xml",'r') as File:
        result = invoice.invoice_upload_API_v2(token, File, filename, "html")
    helper.delFileByPath(f"invoices/{filename}.xml")
    return result