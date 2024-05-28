import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

from src.app import helper
from src.app import error
import re
import hashlib

email_username = "invoicereceivingh18a@gmail.com"
email_pass = 'InvoiceReceiving123'

regex = '^[a-z0-9]+[\\._]?[ a-z0-9]+[@]\\w+[. ]\\w{2,3}$'
session_id = 2021


def auth_register(email, password, username):
    '''
    This function give a username, email address, and password, create a new account for them and return a new token.

    Arguments:
        Parameters:{username: str, email: str, password: str}

    Exceptions:
    InputError when any of:
    • email entered is not a valid email
    • email address is already being used by another user

    Return values:
        {token: str}
    '''
    global session_id
    data = helper.load()
    
    #check email format
    if (not re.search(regex, email)):
        raise error.InputError(description = "Email entered is not a valid email")
    #check email is never been registered
    for user in data['users']:
        if email == user['email']:
            raise error.InputError(description = "Email entered had been registered")
        
    uid = len(data["users"]) + 1
    #generate randon token for user
    session_id += 1
    token = helper.generate_token(uid,session_id)
    #encode password for security reason
    password_encoded = hashlib.sha256(password.encode()).hexdigest()
    #update database
    data["users"].append({
        "uid":uid,
        "username":username,
        "password":password_encoded,
        "email":email,
        "token":token,
        "session_id": session_id,
        "owned_invoices":[],
        "owned_reports":[],
        "total_invoices": 0,
        "reset_code": None
    }
    )
    helper.save(data)
    return token

def auth_login(email, password):
    '''
    Given a registered users' email and password and returns a new `token` for that session.

    Arguments:
        Parameters:{email: str, password: str}

    Exceptions:
    InputError when any of:
    • email entered does not belong to a user
    • password is not correct
    Return Value:
        {token: str}
    '''
    global session_id
    data = helper.load()
    registered = False
    correct_password = False
    password_encoded = hashlib.sha256(password.encode()).hexdigest()
    for user in data["users"]:
        if email == user["email"]:
            registered = True
            if password_encoded == user["password"]:
                correct_password = True
                uid = user["uid"]
                session_id += 1 
                token = helper.generate_token(uid,session_id)
                user["token"] = token
                user["session_id"] = session_id
    #email not registerd
    if registered == False:
        raise error.InputError(description = "email entered does not belong to a user")
    #wrong password
    if correct_password == False:
        raise error.AccessError(description = "password is not correct")
    helper.save(data)
    return token

#Given an active token, invalidates the token to log the user out.
def auth_logout(token):
    '''
    If a valid token is given, then turn the token into None to
    logged out, returns true, otherwise raise AccessError.

    Arguments:
        Parameters:{token: str}

    Exceptions:
    InputError when any of:
    • token entered does not exist

    '''
    data = helper.load()
    helper.check_token(token)
    for user in data['users']:
        if user['token'] == token:
            user['session_id'] = None
            user['token'] = None
            return True
    return False


def auth_password_forgot_request(email):
    '''
    If a valid email is given, then send the reset code to the email

    Arguments:
        Parameters:{email: str}

    Exceptions:
    AccessError when any of:
    • email entered does not exist

    '''
    data = helper.load()
    reset_code = randint(100000, 9999999)

    verified = False
    for user in data["users"]:
        if user["email"] == email:
            verified = True
            user['reset_code'] = str(reset_code)

    if verified is False:
        raise error.AccessError("Unregistered email")

    send_reset_code(email, reset_code)

    helper.save(data)
    return True



def auth_password_reset_reset(email, reset_code, new_password):
    '''
    If a valid email, reset_code is given, then reset the user's password as new_password

    Arguments:
        Parameters:{email: str, reset_code: str, new_password: str}

    Exceptions:
    InputError when any of:
    • reset code entered does not match email

    '''
    data = helper.load()

    # check for valid code
    valid = False
    for user in data["users"]:
        if user["email"] == email and user["reset_code"] ==reset_code and user['reset_code'] is not None:
            user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
            valid = True

    if valid == False:
        raise error.InputError("Invalid code or email")

    helper.save(data)
    return True


def send_reset_code(email, resetcode):
    smtp_server = "smtp.gmail.com"
    subject = f"Password reset code"
    body = f"hello, here is your resetcode: {resetcode}."

    message = MIMEMultipart()
    message["From"] = email_username
    message["To"] = email
    message["Subject"] = subject
    message["Bcc"] = email
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()
    server = smtplib.SMTP_SSL(smtp_server)
    # Sending the email
    try:
        # server.starttls(context=context)
        server.ehlo()
        server.login(email_username, email_pass)
        server.sendmail(email_username, email, text)
        return True
    except:
        return False
    finally:
        server.quit()