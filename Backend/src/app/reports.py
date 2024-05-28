from src.app import error
from src.app import helper

def reports_list(token):
    '''
    Given a token and returns  a list of all reports for that session.
    Arguments:
        Parameters:{token}

    Exceptions:
    InputError when any of:
    • token does not belong to a user
    • owened_reports is not correct
    Return Value:
        {reports}
    '''
    helper.check_token(token)
    uid = helper.getUid(token)
    data = helper.load()
    for user in data["users"]:
        if uid == user['uid']:
            owned_reports = user['owned_reports']
    result = []
    if (owned_reports != None):
        for owened_report in  owned_reports:
            for report in data["reports"]:
                if owened_report["report_id"] == report["report_id"]:
                    result.append({
                        "report_id": owened_report["report_id"],
                        "report_name": report["report_name"]})
    return result

def reports_read(token, report_id):
    '''
    Given a token and invoice_id. then return a report file.

    Arguments:
        Parameters:{token: str, invoice_id: int}

    Exceptions:
    InputError when any of:
    • token does not belong to a user
    • invoice_id is not correct

    Return Value:
        { path }
    '''
    helper.check_token(token)
    uid = helper.getUid(token)
    data = helper.load()
    
    found_report = False
    has_access = False
    fileName = ""
    for report in data["reports"]:
        if report_id == report["report_id"]:
            found_report = True
            if uid == report["user_id"]:
                has_access = True
                fileName = report["report_name"]
                break

    if found_report == False:
        raise error.InputError(description ="report_id doesn't exist")
    if has_access == False:
        raise error.AccessError(description = "Permission denied")
    
    path = f'../../reports/{fileName}'
    return path