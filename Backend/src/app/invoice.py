import random
import zipfile
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os.path
import time
import json
import imaplib
import base64
import os
import email
import glob
import smtplib, ssl
import requests
from smtplib import *

from json2html import *
from src.app import error
from src.app import helper
from src.app import validate
from src.app import storage
from fpdf import FPDF

from datetime import datetime

from src.app.invoices import invoices_read
from src.app import storage
email_username = "invoicereceivingh18a@gmail.com"
email_pass = 'InvoiceReceiving123'
tmp_download_folder = 'tmp_invoices/'


# Receive file from api
# persist file or error and generates the comm report
def invoice_upload_API(token, file, report_type):
    """
          Return the communication report when given a type, invoice_id, token
          The communication report should include the size of file, name, type, sender, time stamp or error

     Arguments:
          Parameters:{token: str, file: str, report_type: str}

     Return Value:
        {report}: json}
     """
    # token validation
    helper.check_token(token)

    # store file into external storage api
    password = storage.store_invoice(file, random.randint(1000,100000))
    file.seek(0)
    # generate report
    report = generate_report(token, file, report_type.lower(), password)
    return report

def invoice_upload_API_v2(token, file, filename,report_type):
    """
          Return the communication report when given a type, invoice_id, token
          The communication report should include the size of file, name, type, sender, time stamp or error

     Arguments:
          Parameters:{token: str, file: str, report_type: str}

     Return Value:
        {report}: json}
     """
    # token validation
    helper.check_token(token)

    # store file into external storage api
    password = storage.store_invoice_v2(file, filename, random.randint(1000,100000))
    file.seek(0)
    # generate report
    report = generate_report_v2(token, file, filename, report_type.lower(), password)
    return report

def storeFile(file):
    """
    store this file to local machine for now(will use storage api in future sprint)
    if there already have file with same file name, and an index at the end of filename. e.g. if file.xml exist then create file(1).xml
    Arguments:
        Parameters:{file: str}

    Return Value:
        {path}: file}
     """
    # open file
    fileName = os.path.basename(file.name)
    fileBase = os.path.splitext(fileName)[0]
    fileExt = os.path.splitext(fileName)[1]
    if fileExt != ".xml":
        raise error.InputError(description="Only support XML file")
    CHECK_FOLDER = os.path.isdir("invoices/")
    if not CHECK_FOLDER:
        os.makedirs("invoices/")
    path = 'invoices/%s%s' % (fileBase, fileExt)
    # write content into file
    with open(path, 'w') as outputFile:
        outputFile.write(file.read())
    file.seek(0)
        
    return os.path.basename(path)


def emailLogin():
    """
    connect email using ssl

    Return Value:
        {mail: str}
    """
    # SSL socket for gmail
    # IMAP
    host = "imap.gmail.com"
    mail = imaplib.IMAP4_SSL(host, 993)
    mail.login(email_username, email_pass)

    return mail


def invoice_upload_imap(token, report_type):
    """
    Get the email sent by the user from the service mailbox, and read the invoice and report type.
    Send back an email with a report file when processing is complete

    Arguments:
        Parameters:{token: str, report_type: str}

    Exceptions:
    AccessError when any of:
    • email connect timeout

    """
    # mail login
    mail = emailLogin()
    helper.check_token(token)
    # While server is running, look for new emails with attachments

    try:
        mail.select("Inbox", readonly=False)
        # search mail for subject of invoice
        # Assuming no other emails are sending to service
        _typ, data = mail.uid('search', 'UNSEEN')
        # Ensure the data is new and not read
        # time.sleep(5)
        for mails in data[0].split():
            if mails != '':
                # Sleep for 1min if no new email is found
                # Cleanse the invoice out from different parts
                _typ, messageComp = mail.uid('fetch', mails, '(RFC822)')
                body = messageComp[0][1]
                # Get email sender
                msg = email.message_from_bytes(body)
                email_sender = msg.get("From")
                email_sender = email_sender.split(' ')
                sender_email = str(email_sender[-1][1:-1])

                # Check storage for email
                token = helper.getTokenByEmail(sender_email)
                if sender_email == helper.getEmail(token):
                    # print(body)
                    email_string = body.decode('utf-8')
                    message = email.message_from_string(email_string)
                    # print(message)
                    CHECK_FOLDER = os.path.isdir(tmp_download_folder)
                    if not CHECK_FOLDER:
                        os.makedirs(tmp_download_folder)
                    result = persistMsg(message, tmp_download_folder)
                    filename = result["fileName"]
                    password = result["password"]
                    # Generate report and send it off
                    report = emailGenReport(open(f"invoices/{filename}","r"), token, report_type, password)
                    sendFile(sender_email, report, report_type)
                    helper.delFileByPath(f"invoices/{filename}")
                    return report
            else:
                raise error.AccessError(description="failed connection")
    except imaplib.IMAP4.error as connect_error:
        raise error.AccessError(description="failed connection") from connect_error


def persistMsg(message, download_folder):
    for part in message.walk():
        fileName = part.get_filename()
        if bool(fileName) and ".xml" in fileName:
            filePath = os.path.join(download_folder, fileName)
            if not os.path.isfile(filePath):
                if part:
                    write_file = open(filePath, 'wb')
                    write_file.write(part.get_payload(decode=True))
                    write_file.close()
                    read_file = open(filePath, 'r')
                    newFileName = storeFile(read_file)
                    read_file.close()
                    password = storage.store_invoice(open(filePath,"r"), random.randint(1000,100000))
                    helper.delFileByPath(filePath)
                    return {"fileName":newFileName,"password":password}


def emailGenReport(file, token, report_type, password):
    # if filenames:
    report = generate_report(token, file, report_type.lower(), password)
    CHECK_FOLDER = os.path.isdir('tmp_reports/')
    if not CHECK_FOLDER:
        os.makedirs('tmp_reports/')
    for f in glob.glob('tmp_reports/*'):
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
    return report


def sendFile(receiver_email, report, report_type):
    # SMTP
    # port = 465
    smtp_server = "smtp.gmail.com"
    # SSL secure connection
    # context = ssl.create_default_context()

    # Message sent to customer (message and set headers)
    subject = "Invoice Received!"
    body = "Dear valued customer, your invoice has been succesfully sent to our systems. Below is a communication report attached."
    message = MIMEMultipart()
    message["From"] = email_username
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    CHECK_FOLDER = os.path.isdir('tmp_reports/')
    if not CHECK_FOLDER:
        os.makedirs('tmp_reports/')

    # Adding body to message
    message.attach(MIMEText(body, "plain"))
    # have to create tmp file to store report json
    if report_type.lower() == "html":
        result = json2htmlformat(report)
    elif report_type == 'json':
        result = str(report)
    with open(f"tmp_reports/Communication_Report.{report_type}", "w") as reportFile:
        reportFile.write(result)

    with open(f"tmp_reports/Communication_Report.{report_type}", "r") as attachment:
        # Email attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    helper.delFileByPath(f"tmp_reports/Communication_Report.{report_type}")

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename = Communication Report.{report_type}"
    )
    message.attach(part)
    text = message.as_string()
    server = smtplib.SMTP_SSL(smtp_server)
    # Sending the email
    try:
        # server.starttls(context=context)
        server.ehlo()
        server.login(email_username, email_pass)
        server.sendmail(email_username, receiver_email, text)
    except SMTPResponseException as e:
        return e.smtp_error
    finally:
        server.quit()


def generate_report(token, invoice, report_type, password):
    '''
    receive file through API CALLS and store in it into /invoices
    insert file into db then delete the file from invoice -- done
    Generate report type given
    insert report into db for future use (saves time from generating new report)

    Arguments:
        Parameters:{token: str, fileName: str, report_type: str}

    Exceptions:
    InputError when any of:
    • token not exit
    • file is not exit
    • report_type is not json/html

    Return Value:
        {report: json}
    '''
    data = helper.load()

    CHECK_FOLDER = os.path.isdir("tmp_invoices/")
    if not CHECK_FOLDER:
        os.makedirs("tmp_invoices/")

    filename = os.path.basename(invoice.name)
    invoice.seek(0)
    with open(f'tmp_invoices/{filename}', 'w') as outputFile:
        outputFile.write(invoice.read())
    invoiceId = len(data["invoices"]) + 1
    reportId = len(data["reports"]) + 1
    fileBase = os.path.splitext(filename)[0]
    fileExt = os.path.splitext(filename)[1]

    fileSize = os.path.getsize(f'tmp_invoices/{filename}')
    timeStampSec = os.path.getctime(f'tmp_invoices/{filename}')
    timeStamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timeStampSec))
    userId = helper.getUid(token)
    userName = helper.getUserName(token)
    #invoice_error = "External Validation API Error"
    invoice_error = validate.validate_invoice1(f'tmp_invoices/{filename}')

    # gereate report fomat
    report = {
        'report_id': reportId,
        'owner_id': userId,
        'owner_username': userName,
        'invoice_id': invoiceId,
        'filename': fileBase,
        'filetype': fileExt,
        'filesize': fileSize,
        'time_stamp': timeStamp,
        'error': invoice_error
    }
    CHECK_FOLDER = os.path.isdir("reports/")
    if not CHECK_FOLDER:
        os.makedirs("reports/")
    # generate communcation report in json
    if report_type == "json":
        report_json = json.dumps(report)
        fileBase = os.path.splitext(fileBase)[0]
        report_path = 'reports/%s%s%s%s%s' % (fileBase, "_report", str(timeStampSec).split(".")[1], invoiceId, ".json")
        with open(report_path, "w") as reportFile:
            reportFile.write(report_json)
    # generate communcation report in html
    elif report_type == "html":
        result_html = json2htmlformat(report)
        fileBase = os.path.splitext(fileBase)[0]
        report_path = 'reports/%s%s%s%s%s' % (fileBase, "_report", str(timeStampSec).split(".")[1], invoiceId, ".html")
        with open(report_path, "w", encoding='utf-8') as reportFile:
            reportFile.write(result_html)

    else:
        raise error.InputError(description="Unsupported report type")
    # save invoice info into database
    data['invoices'].append({
        "invoice_id": invoiceId,
        "filename": filename,
        "report_id": reportId,
        "user_id": helper.getUid(token),
        'password': password,
        'filesize': fileSize,
        'time_stamp': timeStamp
    })
    # save report info into database
    data['reports'].append({
        "report_id": reportId,
        "report_name": '%s%s%s%s.%s' % (fileBase, "_report", str(timeStampSec).split(".")[1], invoiceId, report_type.lower()),
        "invoice_id": invoiceId,
        "user_id": helper.getUid(token)
    })
    for user in data["users"]:
        if userId == user["uid"]:
            user["owned_invoices"].append({"invoice_id": invoiceId})
            user["owned_reports"].append({"report_id": reportId})
            user["total_invoices"] += 1
    # save data
    helper.save(data)
    helper.delFileByPath(f'tmp_invoices/{filename}')
    return report

def generate_report_v2(token, invoice, filename, report_type, password):
    '''
    receive file through API CALLS and store in it into /invoices
    insert file into db then delete the file from invoice -- done
    Generate report type given
    insert report into db for future use (saves time from generating new report)

    Arguments:
        Parameters:{token: str, fileName: str, report_type: str}

    Exceptions:
    InputError when any of:
    • token not exit
    • file is not exit
    • report_type is not json/html

    Return Value:
        {report: json}
    '''
    data = helper.load()

    CHECK_FOLDER = os.path.isdir("tmp_invoices/")
    if not CHECK_FOLDER:
        os.makedirs("tmp_invoices/")

    invoice.seek(0)
    with open(f'tmp_invoices/{filename}.xml', 'w') as outputFile:
        outputFile.write(invoice.read())
    invoiceId = len(data["invoices"]) + 1
    reportId = len(data["reports"]) + 1

    fileSize = os.path.getsize(f'tmp_invoices/{filename}.xml')
    timeStampSec = os.path.getctime(f'tmp_invoices/{filename}.xml')
    timeStamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timeStampSec))
    userId = helper.getUid(token)
    userName = helper.getUserName(token)
    #invoice_error = "External Validation API Error"
    invoice_error = validate.validate_invoice1(f'tmp_invoices/{filename}.xml')

    # gereate report fomat
    report = {
        'report_id': reportId,
        'owner_id': userId,
        'owner_username': userName,
        'invoice_id': invoiceId,
        'filename': filename,
        'filetype': "xml",
        'filesize': fileSize,
        'time_stamp': timeStamp,
        'error': invoice_error
    }
    CHECK_FOLDER = os.path.isdir("reports/")
    if not CHECK_FOLDER:
        os.makedirs("reports/")
    # generate communcation report in json
    if report_type == "json":
        report_json = json.dumps(report)
        report_path = 'reports/%s%s%s%s%s' % (filename, "_report", str(timeStampSec).split(".")[1], invoiceId, ".json")
        with open(report_path, "w") as reportFile:
            reportFile.write(report_json)
    # generate communcation report in html
    elif report_type == "html":
        result_html = json2htmlformat(report)
        report_path = 'reports/%s%s%s%s%s' % (filename, "_report", str(timeStampSec).split(".")[1], invoiceId, ".html")
        with open(report_path, "w", encoding='utf-8') as reportFile:
            reportFile.write(result_html)

    else:
        raise error.InputError(description="Unsupported report type")
    # save invoice info into database
    data['invoices'].append({
        "invoice_id": invoiceId,
        "filename": f"{filename}.xml",
        "report_id": reportId,
        "user_id": helper.getUid(token),
        'password': password,
        'filesize': fileSize,
        'time_stamp': timeStamp
    })
    # save report info into database
    data['reports'].append({
        "report_id": reportId,
        "report_name": '%s%s%s%s.%s' % (filename, "_report", str(timeStampSec).split(".")[1], invoiceId, report_type.lower()),
        "invoice_id": invoiceId,
        "user_id": helper.getUid(token)
    })
    for user in data["users"]:
        if userId == user["uid"]:
            user["owned_invoices"].append({"invoice_id": invoiceId})
            user["owned_reports"].append({"report_id": reportId})
            user["total_invoices"] += 1
    # save data
    helper.save(data)
    helper.delFileByPath(f'tmp_invoices/{filename}.xml')
    return report

def json2htmlformat(report):
    report_json = json.dumps(report)
    hdml_report = json2html.convert(report_json)
    html_head = '''<!DOCTYPE html>
     <html lang="en">
     <head>
          <meta charset="UTF-8">
          <title>Title</title>
     </head>
     <body>
     {}
     </body>
     </html>'''
    result_html = html_head.format(hdml_report)
    return result_html


def rendering_invoice(token, invoice_id):
    '''
    Use the rendering API. Find our XML format from the database by report_id.
    Then send the invoice to the API. The API then returns a rendered invoice in HTML format

    Arguments:
        Parameters:{token: str, invoice_id: int}

    Exceptions:
    • Connection API timed out
    • token is not correct
    • invoice_id is not correct

    Return Value:
        {file_name: html}
    '''
    helper.check_token(token)
    CHECK_FOLDER = os.path.isdir("render/")
    if not CHECK_FOLDER:
        os.makedirs("render/")

    file_content = invoices_read(token, invoice_id)

    with open("tmp_invoices/invoice.xml", "wb") as openfile:
        openfile.write(file_content)

    upload_url = "http://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/upload"
    file_for_rendering = {'file': open("tmp_invoices/invoice.xml", 'r')}
    upload_resp = requests.post(upload_url, files=file_for_rendering)
    if upload_resp.status_code != 200:
        raise error.ConnectionError(description='unable to connect rendering API')

    download_url = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/download"
    result = requests.get(f"{download_url}?file_id={upload_resp.json()['file_ids'][0]}&file_type=HTML")
    
    report_path = 'render/%s%s' % ('temp', ".zip")
    with open(report_path, "wb") as reportFile:
        reportFile.write(result.content)

    with zipfile.ZipFile('render/temp.zip', 'r') as zzz:
        file_name = zzz.namelist()[0]
        zzz.extractall('render')

    helper.delFileByPath('render/temp.zip')

    path = f'../../render/{file_name}'
    return path


def invoice_send(token, invoice_id, recipientEmail):
    '''
    Use the send API. Find our XML format from the database by report_id.
    Then send the invoice and destination email address to the API.
    The API will help to send the invoice to the target email address

    Arguments:
        Parameters:{token: str, invoice_id: int, recipientEmail: str}

    Exceptions:
    • Connection API timed out
    • token is not correct
    • invoice_id is not correct
    Return Value:
    send success:{"state":"success",
                    "sender":username,
                    "recipient email": recipientEmail,
                    "invoice id": invoice_id} 
    send fail: {"state": "fail"} 
    '''
    helper.check_token(token)
    file_content = invoices_read(token, invoice_id)
    username = helper.getUserName(token)
    smtp_server = "smtp.gmail.com"
    subject = f"Invoice from {username}"
    body = f"hello, here is your invoice from {username}."

    message = MIMEMultipart()
    message["From"] = email_username
    message["To"] = recipientEmail
    message["Subject"] = subject
    message["Bcc"] = recipientEmail
    message.attach(MIMEText(body, "plain"))

    with open(f"tmp_invoices/Invoice.xml", "wb") as InvoiceFile:
        InvoiceFile.write(file_content)

    with open(f"tmp_invoices/Invoice.xml", "r") as attachment:
        # Email attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    helper.delFileByPath(f"tmp_invoices/Invoice.xml")
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename = e-invoice.xml"
    )
    message.attach(part)
    text = message.as_string()
    server = smtplib.SMTP_SSL(smtp_server)
    # Sending the email
    try:
        # server.starttls(context=context)
        server.ehlo()
        server.login(email_username, email_pass)
        server.sendmail(email_username, recipientEmail, text)
        return {"state": "success",
                "sender": username,
                "recipient email": recipientEmail,
                "invoice id": invoice_id}
    except:
        return {"state": "fail"}
    finally:
        server.quit()

def invoice_send_v2(token, invoice_id, recipientEmail, filename):
    '''
    Use the send API. Find our XML format from the database by report_id.
    Then send the invoice and destination email address to the API.
    The API will help to send the invoice to the target email address

    Arguments:
        Parameters:{token: str, invoice_id: int, recipientEmail: str}

    Exceptions:
    • Connection API timed out
    • token is not correct
    • invoice_id is not correct
    Return Value:
    send success:{"state":"success",
                    "sender":username,
                    "recipient email": recipientEmail,
                    "invoice id": invoice_id} 
    send fail: {"state": "fail"} 
    '''
    helper.check_token(token)
    file_content = invoices_read(token, invoice_id)
    username = helper.getUserName(token)
    smtp_server = "smtp.gmail.com"
    subject = f"Invoice from {username}"
    body = f"hello, here is your invoice from {username}."

    message = MIMEMultipart()
    message["From"] = email_username
    message["To"] = recipientEmail
    message["Subject"] = subject
    message["Bcc"] = recipientEmail
    message.attach(MIMEText(body, "plain"))

    with open(f"tmp_invoices/Invoice.xml", "wb") as InvoiceFile:
        InvoiceFile.write(file_content)

    with open(f"tmp_invoices/Invoice.xml", "r") as attachment:
        # Email attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    helper.delFileByPath(f"tmp_invoices/Invoice.xml")
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename = {filename}.xml"
    )
    message.attach(part)
    text = message.as_string()
    server = smtplib.SMTP_SSL(smtp_server)
    # Sending the email
    try:
        # server.starttls(context=context)
        server.ehlo()
        server.login(email_username, email_pass)
        server.sendmail(email_username, recipientEmail, text)
        return {"state": "success",
                "sender": username,
                "recipient email": recipientEmail,
                "invoice id": invoice_id}
    except:
        return {"state": "fail"}
    finally:
        server.quit()