import requests
import os
from src.app import error

def store_invoice(invoice,password):
    filename = os.path.basename(invoice.name)
    if os.path.splitext(filename)[1] != ".xml":
         raise error.InputError(description="Please provide XML file")
    file_content = invoice.read()
    file_info = {"FileName":filename,
                "XML":file_content,
                "Password":password}
    storage_url = 'https://teamfudgeh17a.herokuapp.com/store'
    result = requests.post(storage_url,data = file_info)
    if result.status_code == 200:
        return password
    else:
        raise error.ExternalAPIError(description="Something goes wrong with external storage API, please try again!")

def store_invoice_v2(invoice,filename,password):
    upload_filename = os.path.basename(invoice.name)
    if os.path.splitext(upload_filename)[1] != ".xml":
         raise error.InputError(description="Please provide XML file")
    file_content = invoice.read()
    file_info = {"FileName":f"{filename}.xml",
                "XML":file_content,
                "Password":password}
    storage_url = 'https://teamfudgeh17a.herokuapp.com/store'
    result = requests.post(storage_url,data = file_info)
    if result.status_code == 200:
        return password
    else:
        raise error.ExternalAPIError(description="Something goes wrong with external storage API, please try again!")

def extra_invoice(filename, password):
    extra_url = 'https://teamfudgeh17a.herokuapp.com/extract'
    file_info = {"FileName":filename,
                "Password":password}
    result = requests.post(extra_url,data = file_info)
    return result.content

def del_invoice(filename, password):
    del_url = 'https://teamfudgeh17a.herokuapp.com/remove'
    file_info = {"FileName":filename,
                "Password":password}
    result = requests.post(del_url,data = file_info)
    if result.status_code == 200:
        return "Delete Success"
    return "Delete Failure"
