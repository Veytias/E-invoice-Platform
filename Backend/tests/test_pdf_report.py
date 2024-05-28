import pytest
import os
from src.app import invoice
from src.app import reports
from src.app import helper
from src.app import auth
from src.app import error



def test_reports_pdf():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload file
    invoice.invoice_upload_API(token,open("tests/test_files/AU Invoice.xml",'r'), "pdf")


    # get reports list
    result = reports.reports_list(token)
    assert result == [{'report_id': 1, 'report_name': 'AU Invoice_report.pdf'}]

def test_reports_PDF():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "PDF")
    result = reports.reports_list(token)
    assert result == [{'report_id': 1, 'report_name': 'AU Invoice_report.pdf'}]



def test_many_reports_pdf():
    # remove test file(some file may save by other test)
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload 2 file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "pdf")
    invoice.invoice_upload_API(token,open("tests/test_files/test_invoice.xml",'r'), "pdf")

    #get reports list
    result = reports.reports_list(token)
    assert result == [{'report_id': 1, 'report_name': 'AU Invoice_report.pdf'},
                      {'report_id': 2, 'report_name': 'test_invoice_report.pdf'}]



def test_reports_pdf_and_json():
    # remove test file(some file may save by other test)
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload 1 file but need two type of reports
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "pdf")
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "json")

    #get reports list
    result = reports.reports_list(token)
    assert result == [{'report_id': 1, 'report_name': 'AU Invoice_report.pdf'},
                      {'report_id': 2, 'report_name': 'AU Invoice(1)_report.json'}]

