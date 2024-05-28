import pytest
import os
from src.app import invoice
from src.app import reports
from src.app import helper
from src.app import auth
from src.app import error 

def test_reports_list_success():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload file
    invoice.invoice_upload_API(token,  open("tests/test_files/AU Invoice.xml",'r'), "json")
    #get reports list
    result = reports.reports_list(token)
    assert result == [{'report_id': 1, 'report_name': 'AU Invoice_report.json'}]
    

def test_reports_list_success2():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload multiple files
    invoice.invoice_upload_API(token,  open("tests/test_files/AU Invoice.xml",'r'), "json")
    invoice.invoice_upload_API(token,  open("tests/test_files/AU Invoice.xml",'r'), "json")
    #get reports list
    result = reports.reports_list(token)
    assert result == [{'report_id': 1, 'report_name': 'AU Invoice_report.json'},{'report_id': 2, 'report_name': 'AU Invoice(1)_report.json'}]
    
def test_reports_read_success():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload file
    invoice.invoice_upload_API(token,  open("tests/test_files/AU Invoice.xml",'r'), "json")
    #read invoice
    path = reports.reports_read(token, 1)
    #compare result

    assert path =="../../reports/AU Invoice_report.json"
    
def test_reports_read_not_exist():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "json")
    #read invoice
    with pytest.raises(error.InputError):
        reports.reports_read(token, 2)

def test_reports_read_wrong_user():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    token2 = auth.auth_register("testemail2@gmail.com", "6543211","tester2")
    #upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "json")
    #read invoice
    with pytest.raises(error.AccessError):
        reports.reports_read(token2, 1)


