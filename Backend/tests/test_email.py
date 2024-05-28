import smtplib
from smtplib import *
import pytest
from src.app import helper, invoice, reports
from src.app import auth 
import os
import imaplib

# def test_r():
#     helper.clear()
#     token2 = auth.auth_register("tuned_in@outlook.com", "123456","tester1")
#     invoice.invoice_upload_imap(token2)

# def test_receive_invoice():
#     assert os.path.isfile('invoices/REEEE.xml')

# def test_report_generated():
#     assert os.path.isfile('reports/REEEE_report.json')

# Check if there is no invoices left in mailbox
def test_no_invoice():
    helper.clear()
    mail = invoice.emailLogin()
    mail.select("Inbox", readonly=True) 
    _typ, data = mail.search(None, 'X-GM-RAW', 'has:attachment')
    if data[0] == b'':
        exit()

# Pinging the imap server, if error then test fail
def test_imapConnection():
    try:
        invoice.emailLogin()
    except imaplib.IMAP4.error:
        assert False

def test_smtpConnection():
    smtp_server = "smtp.gmail.com"
    server = smtplib.SMTP_SSL(smtp_server)
    try:
        server.ehlo()
        server.login("invoicereceivingh18a@gmail.com", "InvoiceReceiving123")
    except SMTPResponseException as e:
        assert e.smtp_error
    finally:
          server.quit()

