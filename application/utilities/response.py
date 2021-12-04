class Response:
    @staticmethod
    def make(status=True, msg='',data=[]):
        return {'status':status, 'msg':msg, 'data':data}

    @staticmethod
    def datatable(status=True, msg='',data={}):
        response={'status':status, 'msg':msg, 'data':data.get('datas'), 'recordsTotal':data.get('totalRecords')}
        if data.get('totalRecordsFiltered') !=None:
            response.update({'recordsFiltered':data.get('totalRecordsFiltered')})
        else:
            response.update({'recordsFiltered':data.get('totalRecords')})
        return response

    @staticmethod
    def statusAndMsg(status=True,msg=''):
        return {'status':status, 'msg':msg}