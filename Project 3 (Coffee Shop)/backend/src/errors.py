#API Errors
class api_error(Exception): 
    def __init__(self,error,code):
        self.error = error
        self.code = code

class not_found(api_error):
    def __init__(self, error={'status' : "not_found", 'message': 'Nothing was found here.'}):
        self.error = error
        self.code = 404

class unprocessable(api_error):
    def __init__(self, error = {'status': "unprocessable", 'message': "Action is ununprocessable"  }):
        self.error = error
        self.code = 422

class database_error(api_error):
    def __init__(self, error={'status': "database error" , 'message': "Database error"}):
        self.error = error
        self.code = 500


#Authenication Errors
class auth_error(Exception):
    def __init__(self,error,code):
        self.error = error
        self.code = code

class token_expired(auth_error):
    def __init__(self, error= {'status': "token_expired", 'message': "Token is expired"}):
        self.error = error
        self.code = 401

class invalid_claims(auth_error):
    def __init__(self, error= {'status': "invalid_claims", 'message': "The claim is not correct"}):
        self.error = error
        self.code = 401

class  invalid_header(auth_error):
    def __init__(self, error = {'status': "invalid_header", 'message': "Header is invalid, unable to parse token"}):
        self.error = error
        self.code = 401

class invalid_permissions(auth_error):
    def __init__(self, error = {'status': "invalid_permissions", 'message': "Permissions are is invalid, access not granted"}):
        self.error = error
        self.code = 403

