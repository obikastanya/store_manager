from flask import jsonify
from .employeeModel import db,Employee, EmployeeSchema

class EmployeeController:
    def insert(self):
        data=Employee(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=Employee.query.all()
        result=EmployeeSchema(many=True).dump(data)
        return jsonify(result)
    
