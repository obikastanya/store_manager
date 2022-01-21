from datetime import datetime, timedelta
from email import message
from functools import wraps
from bcrypt import checkpw
import jwt
from flask import  request
from flask import redirect,  render_template,abort, make_response
from application.utilities.response import Response

JWT_SECRETKEY='3d768a0f8fe4479cb01e4766613310bb'

class Auth:
    def __init__(self):
        self.__hashPassword=b'$2b$12$1o91McKXCeCdErqTU48ZN./lEVoSnVSW1el6exEJUXsgl48xXafqe'        
        self.__username='SECRET USERNAME'

    def checkAccess(self):
        if self.checkPassword() and self.checkUsername():
            user=User()
            token=AuthToken().createToken(user)
            return self.successLogin(token)
        else:
            return self.unAuthorizedLogin()

    def checkPassword(self):
        # encode to convert code into universal code /utf-8
        userPassword=request.form.get('password','').encode('UTF-8')
        if checkpw(userPassword, self.__hashPassword):
            return True
        return False
    
    def checkUsername(self):
        username=request.form.get('username','')
        if self.__username==username:
            return True
        return False

    def successLogin(self, token):
        response=make_response(redirect('/'))
        response.set_cookie('x-auth-token', token)
        return response

    def unAuthorizedLogin(self):
        msg="Username or Password is Incorrect"
        return render_template('login.html', msg=msg)
    
    def logOut(self):
        resp=make_response(redirect('/login'))
        resp.delete_cookie('x-auth-token')
        return resp
    


class AuthToken:
    def createToken(self, user):
        token=jwt.encode(
            payload={
                'userId':user.userId,
                'exp':datetime.utcnow() + timedelta(minutes=30)
            },
            key=JWT_SECRETKEY,
            algorithm='HS256')
        return token

    def authenticate(self,func):
        @wraps(func)
        def decorated(**kwargs):
            token=request.cookies.get('x-auth-token')
            if not token:
                return redirect('/login')

            try:
                # check if jwt is active
                jwt.decode(token,JWT_SECRETKEY,algorithms='HS256')
                user=User()
                kwargs=user.__dict__
            except jwt.ExpiredSignatureError:
                return redirect('/login')
            except jwt.InvalidTokenError:
                return abort(400)

            return func(**kwargs)
        return decorated
    
    def noTokenRequired(self,func):
        @wraps(func)
        def decorated(**kwargs):
            try:
                token=request.cookies.get('x-auth-token')
                jwt.decode(token,JWT_SECRETKEY,algorithms='HS256')
                user=User()
                kwargs=user.__dict__
            except:
                return func(**kwargs)
            return redirect('/')

            
        return decorated

    def middleware(self, func):
        @wraps(func)
        def decorated(**kwargs):
            token=request.cookies.get('x-auth-token')
            if not token:
                return Response.make(False,'Forbidden access')

            try:
                jwt.decode(token, JWT_SECRETKEY, algorithms='HS256')
                user=User()
                kwargs=user.__dict__
            except jwt.ExpiredSignatureError:
                return Response.make(False, 'Unauthorized')
            except jwt.InvalidTokenError:
                return Response.make(False, 'Bad Request')
            return func(**kwargs)

        return decorated

class User:
    def __init__(self):
        self.userId='123458667'
        self.firstName='Obi'
        self.lastName='kastanya'
        self.job='Python Programmer'
        self.role='ALL'
        
