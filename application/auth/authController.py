from bcrypt import checkpw
from flask import request, render_template

class Auth:
    def __init__(self):
        self.__hashPassword=b'$2b$12$1o91McKXCeCdErqTU48ZN./lEVoSnVSW1el6exEJUXsgl48xXafqe'
        self.__username='SECRET USERNAME'

    def checkAccess(self):
        if self.checkPassword() and self.checkUsername():
            return self.successLogin()
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

    def successLogin(self):
        return render_template('dashboard.html')

    def unAuthorizedLogin(self):
        msg="Username or Password is Incorrect"
        return render_template('login.html', msg=msg)

