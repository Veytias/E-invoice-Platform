import os

from src.app import error
from src.app import helper
from src.app import invoice
from src.app import storage

def invoices_list(token):
    '''
    Given a token and returns  a list of all invoices for that session.
    Arguments:
        Parameters:{token}

    Exceptions:
    InputError when any of:
    • token does not belong to a user
    • owned_reports is not correct
    Return Value:
        { invoices }
    '''
    helper.check_token(token)
    uid = helper.getUid(token)
    data = helper.load()
    for user in data["users"]:
        if uid == user['uid']:
            owned_reports = user['owned_invoices']
    result = []

    if (owned_reports != None):
        for owened_invoice in owned_reports:
            for invoice in data["invoices"]:
                if owened_invoice["invoice_id"] == invoice["invoice_id"]:
                    result.append({
                        "invoice_id": owened_invoice["invoice_id"],
                        "filename": invoice["filename"],
                        "filesize": invoice["filesize"],
                        "time_stamp": invoice["time_stamp"]})
    return result


def invoices_read(token, invoice_id):
    '''
    Given a token and incoice_id. then returns  the invoice in database.

    Arguments:
        Parameters:{token: str, invoice_id: int}

    Exceptions:
    InputError when any of:
    • token does not belong to a user
    • invoice_id is not correct

    Return Value:
        { path: str }
    '''
    helper.check_token(token)
    uid = helper.getUid(token)
    data = helper.load()

    found_invoice = False
    has_access = False
    fileName = ""
    for curr_invoice in data["invoices"]:
        if invoice_id == curr_invoice["invoice_id"]:
            found_invoice = True
            if uid == curr_invoice["user_id"]:
                has_access = True
                fileName = curr_invoice["filename"]
                password = curr_invoice["password"]
                break
    if found_invoice == False:
        raise error.InputError(description="Invoice_id doesn't exist")
    if has_access == False:
        raise error.AccessError(description="Permission denied")

    file_content = storage.extra_invoice(fileName,password)
    return file_content

def invoices_remove(token, invoice_id):
    '''
    Given a token and invoice_id.
    then remove the invoice information in database and invoice file in folder.

    Arguments:
        Parameters:{token: str, invoice_id: int}

    Exceptions:
    InputError when any of:
    • token does not belong to a user
    • invoice_id is not correct

    Return Value:
        {"state":"success"}
    '''
    helper.check_token(token)
    uid = helper.getUid(token)

    data = helper.load()

    found_invoice = False
    has_access = False
    # invoice_id = 0
    index = 0
    invoice_user_id_save = -1
    invoice_id_save = -1
    invoice_report_id_save = -1
    invoice_filename_save = None
    for invoice in data["invoices"]:
        if invoice_id == invoice["invoice_id"]:
            found_invoice = True
            if uid == invoice["user_id"]:
                has_access = True
                invoice_id_save = invoice["invoice_id"]
                invoice_filename_save = invoice["filename"]
                invoice_report_id_save = invoice["report_id"]
                invoice_user_id_save = invoice["user_id"]
                invoice_password_save = invoice["password"]
                data["invoices"].pop(index)
                break
        index += 1

    index = 0
    for users in data["users"]:
        if invoice_user_id_save == users["uid"]:
            for owned_invoices in users["owned_invoices"]:
                if invoice_id_save == owned_invoices["invoice_id"]:
                    users["owned_invoices"].pop(index)
                    users["owned_reports"].pop(index)
                    users["total_invoices"] -= 1
                    break
                index += 1

    index = 0
    for reports in data["reports"]:
        if invoice_report_id_save == reports["report_id"]:
            invoice_report_file_save = reports["report_name"]
            data["reports"].pop(index)
            break
        index += 1

    if found_invoice == False:
        raise error.InputError(description="Invoice_id does not exist")
    if has_access == False:
        raise error.AccessError(description="Permission denied")

    helper.save(data)
    report_path = f'reports/{invoice_report_file_save}'
    os.remove(report_path)
    result = storage.del_invoice(invoice_filename_save,invoice_password_save)

    return result

