from flask import jsonify
from .statusEmployeeModel import db,StatusEmployee, StatusEmployeeSchema

class StatusEmployeeController:
    def insert(self):
        data=StatusEmployee(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=StatusEmployee.query.all()
        result=StatusEmployeeController(many=True).dump(data)
        return jsonify(result)
    
