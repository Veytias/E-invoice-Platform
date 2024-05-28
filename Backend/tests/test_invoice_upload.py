import pytest
import os
from src.app import invoice
from src.app import helper
from src.app import auth
from src.app import error 

def test_upload_invoice_by_API_call_success():
    helper.clear()
    helper.delFile()
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml","r"),"json")
    data = helper.load()
    
    assert (data['invoices'] ==  [{"invoice_id": 1, "filename": "AU Invoice.xml", "report_id": 1, "user_id": 1}])
    assert (data['reports'] == [{"report_id": 1, "report_name": "AU Invoice_report.json", "invoice_id": 1, "user_id": 1}])
    assert (data['users'][0]['owned_invoices'] == [{"invoice_id": 1}])
    assert (data['users'][0]['owned_reports'] == [{"report_id": 1}])
    
def test_upload_invoice_by_two_or_more_users():
    helper.clear()
    helper.delFile()
    token1 = auth.auth_register("testemail@gmail.com", "123456","tester1")
    token2 = auth.auth_register("testemailiowerjfesdjf@gmail.com", "12345665654", "tester2")


    invoice.invoice_upload_API(token1, open("tests/test_files/AU Invoice.xml","r"),"json")
    invoice.invoice_upload_API(token2, open("tests/test_files/AU Invoice.xml","r"),"json")

    data = helper.load()

    assert (data['invoices'] == [{"invoice_id": 1, "filename": "AU Invoice.xml", "report_id": 1, "user_id": 1},
           {"invoice_id": 2, "filename": "AU Invoice(1).xml", "report_id": 2, "user_id": 2}])
    assert (data['reports'] == [{"report_id": 1, "report_name": "AU Invoice_report.json", "invoice_id": 1, "user_id": 1},
                               {"report_id": 2, "report_name": "AU Invoice(1)_report.json", "invoice_id": 2, "user_id": 2}])
    assert (data['users'][0]['owned_invoices'] == [{"invoice_id": 1}])
    assert (data['users'][1]['owned_invoices'] == [{"invoice_id": 2}])
    
    assert (data['users'][0]['owned_reports'] == [{"report_id": 1}])
    assert (data['users'][1]['owned_invoices'] == [{"invoice_id": 2}])
    
    
def test_upload_non_xml_file():
    helper.clear()
    helper.delFile() 
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    with pytest.raises(error.InputError):

        invoice.invoice_upload_API(token, open("tests/test_files/nojson.txt","r"),"json") 

