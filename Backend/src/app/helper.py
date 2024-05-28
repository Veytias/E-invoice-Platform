import jwt
import os
import json
from src.app.error import AccessError, InputError


def load():
    '''
    load the data from the database
    '''
    try:
        with open('database.json', 'r') as FILE:
            data = json.load(FILE)
    except:
        with open('database.json', 'w') as FILE:
            data = json.load(FILE)
    return data

def save(data):
    '''
    save the data in the database

    Arguments:
        Parameters:{data: list}

    '''
    with open('database.json', 'w') as FILE:
        json.dump(data, FILE)
    return data

def clear():
    '''
    clear the data in the database

    Return values:
        {data: list}
    '''
    data = {"users":[],"invoices":[],"reports":[]}
    save(data)
    return data

def delFile():
    '''
    delete all tests generated file
    '''
    dir = "invoices/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
        
    dir = "reports/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    dir = "render/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))



def delFileByPath(File):
    '''
    remove the filepath in file

    Arguments:
        Parameters:{filepath: str}

    '''
    if os.path.exists(File):
        os.remove(File)

    

        
def getUid(token):
    '''
    return u_id for a specific token

    Arguments:
        Parameters:{token: str}

    Exceptions:
    • token entered is not a valid token

    Return values:
        {UID: int}

    '''
    data = load()
    for user in data["users"]:
        if str(token) == user["token"]:
            return user["uid"]
    return None

def getUserName(token):
    '''
    return username for a specific token

    Arguments:
        Parameters:{token: str}

    Exceptions:
    • token entered is not a valid token

    Return values:
        {username: str}
    '''
    data = load()
    for user in data["users"]:
        if str(token) == user["token"]:
            return user["username"]
    return None



secret = 'brownie'

def generate_token(uid,session_id):
    '''
    creating a token

    Arguments:
        Parameters:{uid: int, session_id: int}

    Return values:
        {token: str}

    '''
    user = {'uid': uid,'session_id':session_id}
    return jwt.encode(user, secret, algorithm='HS256')


def check_token(token):
    '''
    check if a token is valid

    Arguments:
        Parameters:{token: str}

    Exceptions:
    AccessError when any of:
    • token entered is not a valid token
    • token is not exist

    '''
    data = load()
    try:
        jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError as invalid_token:
        raise AccessError(description= "invalid token") from invalid_token    
    except jwt.exceptions.DecodeError as token_not_exist:
        raise AccessError(description= "token decode error") from token_not_exist
    
        
    user_data = jwt.decode(token, secret, algorithms=['HS256'])
    uid = user_data["uid"]
    session_id = user_data["session_id"]
    for user in data['users']:
        if token == user['token'] and uid == user['uid'] and session_id == user['session_id']:
            return {'uid': uid,'session_id':session_id}
    raise AccessError(description= "token invalid")
    
    


def getTokenByEmail(email):
    ''''
    return user's token for a specific email

    Arguments:
        Parameters:{email: str}

    Exceptions:
        • email is not exist

    Return values:
        {token: str}
    '''
    data = load()
    for user in data["users"]:
        if email == user["email"]:
            return user["token"]
    return None

def getEmail(token):
    '''
    return user's email for a specific token

    Arguments:
        Parameters:{token: str}

    Exceptions:
        • token is not exist

    Return values:
        {email: str}
    '''
    data = load()
    for user in data["users"]:
        if token == user["token"]:
            return user["email"]
    return None

def getTotalInvoice(token):
    '''
    return user's email for a specific token

    Arguments:
        Parameters:{token: str}

    Exceptions:
        • token is not exist

    Return values:
        {total_invoice_number: int}
    '''
    data = load()
    for user in data["users"]:
        if token == user["token"]:
            return user["total_invoices"]
    return None
