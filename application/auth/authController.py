from datetime import datetime, timedelta
from functools import wraps
from bcrypt import checkpw
import jwt
from flask import  redirect, request, render_template,abort, make_response, url_for

JWT_SECRETKEY='3d768a0f8fe4479cb01e4766613310bb'

class Auth:
    def __init__(self):
        self.__hashPassword=b'$2b$12$1o91McKXCeCdErqTU48ZN./lEVoSnVSW1el6exEJUXsgl48xXafqe'
        
        self.__username='SECRET USERNAME'


    def logOut(self):
        pass

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
        def decorated(**kwargs):
            # print(request.cookies.get('x-auth-token'))
            token=None
            token=request.cookies.get('x-auth-token')
            if not token:
                return abort(401)

            # try:
            data=jwt.decode(token,JWT_SECRETKEY,algorithms='HS256')
            user=User()
            # except:
                # jwt in expired
            # return abort(401)

            return func(**{'name':user.firstName})
        return decorated


    def middleware(self, func):
        @wraps
        def decorated(*args,**kwargs):
            token=None
            if 'x-access-token' in request.headers:
                token=request.headers.get('x-access-token')
            if not token:
                return {'msg':'Token is missing !!'}
            try:
                data=jwt.decode(token, JWT_SECRETKEY)
                user=User()
            except:
                return {'msg':'token is invalid'}
            return func(user,*args, **kwargs)
        return decorated

class User:
    def __init__(self):
        self.userId='123458667'
        self.firstName='Obi'
        self.lastName='kastanya'
        self.job='Python Programmer'
        self.role='ALL'
        
