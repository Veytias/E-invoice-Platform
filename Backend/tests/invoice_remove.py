import pytest
import os
from src.app import invoice, invoices
from src.app import reports
from src.app import helper
from src.app import auth
from src.app import error


def test_invoice_remove():
    helper.clear()
    helper.delFile()
    # register user
    token = auth.auth_register("testemail@gmail.com", "123456", "tester1")
    # upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml", 'r'), "json")
    invoice.invoice_upload_API(token, open("tests/test_files/test_invoice.xml", 'r'), "json")

    invoices.invoices_remove(token, 2)

    # get data
    data = helper.load()

    invoice_path = 'invoices/test_invoice.xml'
    report_path = 'reports/test_invoice.json'

    assert (data['invoices'] == [{"invoice_id": 1, "filename": "AU Invoice.xml", "report_id": 1, "user_id": 1}])
    assert (data['reports'] == [{'report_id': 1, 'report_name': 'AU Invoice_report.json', 'invoice_id': 1, 'user_id': 1}])

    assert not os.path.exists(invoice_path)
    assert not os.path.exists(report_path)

def test_invoice_remove_many_user():
    helper.clear()
    helper.delFile()
    # register user
    token = auth.auth_register("testemail@gmail.com", "123456", "tester1")
    # upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml", 'r'), "json")
    invoice.invoice_upload_API(token, open("tests/test_files/test_invoice.xml", 'r'), "json")

    token2 = auth.auth_register("testemail1@gmail.com", "1234561", "tester2")
    invoice.invoice_upload_API(token2, open("tests/test_files/AU Invoice.xml", 'r'), "json")

    invoices.invoices_remove(token, 2)

    # get data
    data = helper.load()

    invoice_path = 'invoices/test_invoice.xml'
    report_path = 'reports/test_invoice.json'

    assert (data['invoices'] == [{"invoice_id": 1, "filename": "AU Invoice.xml", "report_id": 1, "user_id": 1},
                                 {'invoice_id': 3, 'filename': 'AU Invoice(1).xml', 'report_id': 3, 'user_id': 2}])
    assert (data['reports'] == [{'report_id': 1, 'report_name': 'AU Invoice_report.json', 'invoice_id': 1, 'user_id': 1},
                                {'report_id': 3, 'report_name': 'AU Invoice(1)_report.json', 'invoice_id': 3, 'user_id': 2}])

    assert not os.path.exists(invoice_path)
    assert not os.path.exists(report_path)