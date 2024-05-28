import os
from src.app import helper, auth, invoice, reports


def test_invoice_render():
    helper.clear()
    helper.delFile()
    #register user
    token = auth.auth_register("testemail@gmail.com", "123456","tester1")
    #upload file
    invoice.invoice_upload_API(token, open("tests/test_files/AU Invoice.xml",'r'), "html")

    filename = invoice.rendering_invoice(token, 1)
    report_path = 'render/%s' % (filename)

    assert os.path.exists(report_path)

