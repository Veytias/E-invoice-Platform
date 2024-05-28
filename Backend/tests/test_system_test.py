import pytest
from src.app import helper, auth, invoice, reports
from src.app.auth import auth_logout


def test_system():
    helper.clear()
    helper.delFile()
    # register user
    auth.auth_register("testemail@gmail.com", "123456", "tester1")

    # login
    token = auth.auth_login("testemail@gmail.com", "123456")

    # logout
    auth_logout(token)
    data = helper.load()
    assert data["users"][0]["token"] is not token

    # login
    token2 = auth.auth_login("testemail@gmail.com", "123456")

    # upload invoice by api
    # get json report
    invoice.invoice_upload_API(token2, open("tests/test_files/AU Invoice.xml",'r'), "json")

    # check the database in system
    data = helper.load()
    assert (data['invoices'] == [{"invoice_id": 1, "filename": "AU Invoice.xml", "report_id": 1, "user_id": 1}])
    assert (data['reports'] == [
        {"report_id": 1, "report_name": "AU Invoice_report.json", "invoice_id": 1, "user_id": 1}])
    assert (data['users'][0]['owned_invoices'] == [{"invoice_id": 1}])
    assert (data['users'][0]['owned_reports'] == [{"report_id": 1}])

    # get pdf report
    invoice.invoice_upload_API(token2,open("tests/test_files/AU Invoice.xml",'r'), "pdf")

    # check the report information
    result = reports.reports_list(token2)
    assert result == [{'report_id': 1, 'report_name': 'AU Invoice_report.json'},
                      {'report_id': 2, 'report_name': 'AU Invoice(1)_report.pdf'}]

    # check the database in system
    data = helper.load()
    assert (data['invoices'] == [{"invoice_id": 1, "filename": "AU Invoice.xml", "report_id": 1, "user_id": 1},
                                 {"invoice_id": 2, "filename": "AU Invoice(1).xml", "report_id": 2, "user_id": 1}])

    # get html report
    invoice.invoice_upload_API(token2,open("tests/test_files/AU Invoice.xml",'r'), "html")

    # check the report information
    result = reports.reports_list(token2)
    assert result == [{'report_id': 1, 'report_name': 'AU Invoice_report.json'},
                      {'report_id': 2, 'report_name': 'AU Invoice(1)_report.pdf'},
                      {'report_id': 3, 'report_name': 'AU Invoice(2)_report.html'}]

    # check the database in system
    data = helper.load()
    assert (data['invoices'] == [{"invoice_id": 1, "filename": "AU Invoice.xml", "report_id": 1, "user_id": 1},
                                 {"invoice_id": 2, "filename": "AU Invoice(1).xml", "report_id": 2, "user_id": 1},
                                 {"invoice_id": 3, "filename": "AU Invoice(2).xml", "report_id": 3, "user_id": 1}])

    # logout
    auth_logout(token2)

    # login to test the file still exist
    token3 = auth.auth_login("testemail@gmail.com", "123456")
    result = reports.reports_list(token3)
    assert result == [{'report_id': 1, 'report_name': 'AU Invoice_report.json'},
                      {'report_id': 2, 'report_name': 'AU Invoice(1)_report.pdf'},
                      {'report_id': 3, 'report_name': 'AU Invoice(2)_report.html'}]

    # logout
    auth_logout(token3)

    # register another user
    auth.auth_register("test@gmail.com", "1234567", "tester2")

    # login
    token4 = auth.auth_login("test@gmail.com", "1234567")

    # check user2 can't check the invoice for user 1
    result = reports.reports_list(token4)
    assert not result

    # upload another invoice
    invoice.invoice_upload_API(token4, open("tests/test_files/test_invoice.xml",'r'), "html")

    # check the report
    result = reports.reports_list(token4)
    assert result == [{'report_id': 4, 'report_name': 'test_invoice_report.html'}]

    # check have all invoice
    data = helper.load()
    assert (data['invoices'] == [{"invoice_id": 1, "filename": "AU Invoice.xml", "report_id": 1, "user_id": 1},
                                 {"invoice_id": 2, "filename": "AU Invoice(1).xml", "report_id": 2, "user_id": 1},
                                 {"invoice_id": 3, "filename": "AU Invoice(2).xml", "report_id": 3, "user_id": 1},
                                 {"invoice_id": 4, "filename": "test_invoice.xml", "report_id": 4, "user_id": 2}])

    # logout
    auth_logout(token4)
