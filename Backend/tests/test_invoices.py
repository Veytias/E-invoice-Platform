import pytest
import os
from src.app import invoice
from src.app import invoices
from src.app import helper
from src.app import auth 
from src.app import error


def test_invoices_list_success():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "json")
    #get invoices list
    result = invoices.invoices_list(token)
    assert result == [{'invoice_id': 1, 'filename': 'AU Invoice.xml'}]
    

def test_invoices_list_success2():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload multiple files
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "json")
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "json")
    #get invoices list
    result = invoices.invoices_list(token)
    assert result == [{'invoice_id': 1, 'filename': 'AU Invoice.xml'},{'invoice_id': 2, 'filename': 'AU Invoice(1).xml'}]
    
    
def test_invoices_read_success():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "json")
    #read invoice
    path = invoices.invoices_read(token, 1)
    
    assert path == "../../invoices/AU Invoice.xml"
    
def test_invoices_read_not_exist():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "json")
    #read invoice
    with pytest.raises(error.InputError):
        f = invoices.invoices_read(token, 2)
        f.close()

def test_invoices_read_wrong_user():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    token2 = auth.auth_register("testemail2@gmail.com", "6543211","tester2")
    #upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "json")
    #read invoice
    with pytest.raises(error.AccessError):
        f = invoices.invoices_read(token2, 1)
        f.close()

