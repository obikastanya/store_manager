class Response:
    @staticmethod
    def make(status=True, msg='',data=[],):
        return {'status':status, 'msg':msg, 'data':data}

    @staticmethod
    def statusAndMsg(status=True,msg=''):
        return {'status':status, 'msg':msg}