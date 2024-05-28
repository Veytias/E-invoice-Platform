import pytest
#from auth import auth_register, auth_login, auth_logout,auth_passwordrequest,auth_passwordreset,find_user
from src.app import error
from src.app import helper
from src.app import auth

# auth_register
# Email Invalid Tests (Email entered is a valid email by provided method)
def test_register_invalid_domain_email():
    helper.clear()
    with pytest.raises(error.InputError):
        auth.auth_register("wrongEmail", "823745897",  "names")


# Email used by another user 

def test_email_used():
    helper.clear()
    auth.auth_register("invioceuser@gmail.com", "823745897", "names")
    with pytest.raises(error.InputError):
        auth.auth_register("invioceuser@gmail.com", "78947897", "CPU")
        
def test_register_success():
    helper.clear()
    auth.auth_register("invioceuser@gmail.com", "823745897", "names")
    data = helper.load()
    assert data["users"][0]["email"] == "invioceuser@gmail.com"
    assert data["users"][0]["username"] == "names"
#auth_login         

# Wrong password Tests 

def test_login_wrong_password():
    helper.clear()
    auth.auth_register("invioceuser@gmail.com", "823745897", "names")
    with pytest.raises(error.AccessError):
        auth.auth_login("invioceuser@gmail.com", "78947897")
        
def test_login_success():
    helper.clear()
    auth.auth_register("invioceuser@gmail.com", "823745897", "names")
    token = auth.auth_login("invioceuser@gmail.com", "823745897")
    data = helper.load()
    assert data["users"][0]["token"] == str(token)