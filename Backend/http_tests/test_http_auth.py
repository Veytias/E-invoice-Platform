
import requests
from src.app import config
BASE_URL =  config.url

'''
auth_login server testing functions
'''

'''
test 1: Email entered is not registered
'''

def test_login_email_not_registered(): 
    
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")
    
    #test login in server
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
    })
    assert login_resp.status_code == 400

'''
test 2: Password is not correct
'''

def test_login_password_incorrect():
    
    requests.delete(f"{BASE_URL}/clear")
    # register in server
    requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    
    #test login in server
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={
        'email': 'z5331259@gmail.com',
        'password': '1234567890',
    })
    assert login_resp.status_code == 403

'''
test 3: Login successful
'''

def test_login_successful():
    '''
    test if login works on server
    
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear")
    
    #register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'testemail@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    payload = register_resp.json()

    #test logout in server
    requests.post(f"{BASE_URL}/auth/logout", json= {'token': payload})

    #test login in server
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={
        'email': 'testemail@gmail.com',
        'password': 'z5331259',
    })


    assert login_resp.status_code == 200

'''
auth_register server testing functions
'''
'''
test 1: Email entered is not a valid email
'''
def test_register_email_invalid():
    
    
    requests.delete(f"{BASE_URL}/clear")
    
    # register invalid email in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail',
        'password': 'z5331259',
        'username': 'King'
    })
    
    assert register_resp.status_code == 400

'''
test 2: Email address is already being used by another user
'''
def test_register_email_used():
    
    
    requests.delete(f"{BASE_URL}/clear")
    
    # register email in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    
    assert register_resp.status_code == 200

    # register used email in server
    register_resp_2 = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    
    assert register_resp_2.status_code == 400

'''
test 3: user register successful
'''        
def test_register_success():
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    #register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
        'username': 'King'
    })
    payload = register_resp.json()

    #test logout in server
    requests.post(f"{BASE_URL}/auth/logout", json= {'token': payload})


    #test login in server
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={
        'email': 'z5331259@gmail.com',
        'password': 'z5331259',
    })

    assert login_resp.status_code == 200