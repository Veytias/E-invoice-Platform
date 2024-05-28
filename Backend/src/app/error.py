from werkzeug.exceptions import HTTPException

class InputError(HTTPException):
    code = 400
    message = 'Invaild input'
    
class AccessError(HTTPException):
    code = 403
    message = 'Access denied.'

class ConnectionError(HTTPException):
    code = 404
    message = 'Fail upload'

class ExternalAPIError(HTTPException):
    code = 503
    message = "External API error" 


