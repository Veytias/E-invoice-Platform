import sys
import signal
from json import dumps, load
from flask import Flask, request, send_file, abort, Response
from flask_cors import CORS
from src.app.error import InputError
from src.app.error import AccessError
from src.app import config
from src.app import auth
from src.app import invoice
from src.app import invoices
from src.app import reports
from src.app import helper
from src.app import create
from io import BytesIO
from werkzeug.wsgi import FileWrapper

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'APPlication/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


@APP.route('/')
def index():
    return "Hello!"

# Auth
@APP.route("/auth/register", methods=['POST'])
def auth_register():
    data = request.get_json()
    return dumps(auth.auth_register(data['email'],data['password'], data['username']))

@APP.route("/auth/login", methods=['POST'])
def auth_login():
    data = request.get_json()
    return dumps(auth.auth_login(data['email'], data['password']))

@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    data = request.get_json()
    return dumps(auth.auth_logout(data['token']))

@APP.route("/auth/total_invoice", methods=['GET'])
def auth_countInvoices():
    token = request.args.get('token')
    return dumps(helper.getTotalInvoice(token))

@APP.route("/auth/email", methods=['GET'])
def auth_email():
    token = request.args.get('token')
    return dumps(helper.getUserName(token))

@APP.route("/auth/username", methods=['GET'])
def auth_username():
    token = request.args.get('token')
    return dumps(helper.getEmail(token))

@APP.route("/auth/forgot_password", methods=['POST'])
def auth_forgot_passord():
    data = request.get_json()
    return dumps(auth.auth_password_forgot_request(data['email']))

@APP.route("/auth/reset_password", methods=['POST'])
def auth_reset_password():
    data = request.get_json()
    return dumps(auth.auth_password_reset_reset(data['email'], data['reset_code'], data['new_password']))
# Invoice
@APP.route("/invoice/upload/API", methods=['POST'])
def invoice_upload_API():
    file = request.files['file']
    file.save(f'invoices/{file.filename}')
    token = request.form['token']

    report_type = request.form['report_type']
    #token = load(request.files['token'])    
    #report_type = load(request.files['report_type']) 
    result = invoice.invoice_upload_API(token, open(f'invoices/{file.filename}','r'), report_type)   
    helper.delFileByPath(f'invoices/{file.filename}')
    return dumps(result)

@APP.route("/invoice/upload/API/v2", methods=['POST'])
def invoice_upload_API_v2():
    file = request.files['file']
    file.save(f'invoices/{file.filename}')
    token = request.form['token']
    filename = request.form['filename']

    report_type = request.form['report_type']
    result = invoice.invoice_upload_API_v2(token, open(f'invoices/{file.filename}','r'), filename, report_type)   
    helper.delFileByPath(f'invoices/{file.filename}')
    return dumps(result)

@APP.route("/invoice/upload/IMAP", methods=['POST'])
def invoice_upload_imap():
    data = request.get_json()
    return dumps(invoice.invoice_upload_imap(data['token'],data['report_type']))

@APP.route("/invoice/create", methods=['POST'])
def invoice_create():
    file = request.files['file']
    file.save(f'invoices/{file.filename}')
    token = request.form['token']
    result = create.create_invoice(token, open(f'invoices/{file.filename}','r'))
    helper.delFileByPath(f'invoices/{file.filename}')
    return dumps(result)

@APP.route("/invoice/create/v2", methods=['POST'])
def invoice_create_v2():
    file = request.files['file']
    file.save(f'invoices/{file.filename}')
    filename = request.form['filename']
    token = request.form['token']
    result = create.create_invoice_v2(token, filename, open(f'invoices/{file.filename}','r'))
    helper.delFileByPath(f'invoices/{file.filename}')
    return dumps(result)
# Invoices
@APP.route("/invoices/list", methods=['GET'])
def invoices_list():
    token = request.args.get('token')
    return dumps(invoices.invoices_list(token))

@APP.route("/invoices/read", methods=['GET'])
def invoices_read():
    token = request.args.get('token')
    invoice_id = request.args.get('invoice_id')
    result = invoices.invoices_read(token, int(invoice_id))
    file_byte = BytesIO(result)
    file_wrapper = FileWrapper(file_byte)
    try:
        return Response(file_wrapper, mimetype="text/xml", direct_passthrough=True)
    except FileNotFoundError:
        abort(404)

@APP.route("/invoices/remove", methods=['DELETE'])
def invoices_remove():
    data = request.get_json()
    result = invoices.invoices_remove(data['token'], int(data['invoice_id']))
    return dumps(result)

# Reports
@APP.route("/reports/list", methods=['GET'])
def reports_list():
    token = request.args.get('token')
    return dumps(reports.reports_list(token))

@APP.route("/reports/read", methods=['GET'])
def reports_read():
    token = request.args.get('token')
    report_id = request.args.get('report_id')
    result = reports.reports_read(token, int(report_id))
    try:
        if "json" in result:
            return send_file(result,attachment_filename="report.json")
        elif "html" in result:
            return send_file(result,attachment_filename="report.html")
    except FileNotFoundError:
        abort(404)

# Clear
@APP.route("/clear", methods=['DELETE'])
def clear():
    helper.clear()
    helper.delFile()
    return dumps({})

# Other API
@APP.route("/invoices/render", methods=['GET'])
def render_invoice():
    token = request.args.get('token')
    invoice_id = request.args.get('invoice_id')
    result = invoice.rendering_invoice(token, int(invoice_id))
    try:
        return send_file(result,attachment_filename="invoice.html")
    except FileNotFoundError:
        abort(404)


@APP.route("/invoice/send", methods=['POST'])
def send_invoice():
    data = request.get_json()
    return dumps(invoice.invoice_send(data['token'],int(data['invoice_id']),data['recipientEmail']))

@APP.route("/invoice/send/v2", methods=['POST'])
def send_invoice_v2():
    data = request.get_json()
    return dumps(invoice.invoice_send_v2(data['token'],int(data['invoice_id']),data['recipientEmail'], data['filename']))

if __name__ == "__main__":
    APP.run(port=config.port,debug = True)

