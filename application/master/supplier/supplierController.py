from flask import jsonify
from .supplierModel import db,Supplier, SupplierSchema

class SupplierController:
    def insert(self):
        data=Supplier(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=Supplier.query.all()
        result=SupplierSchema(many=True).dump(data)
        return jsonify(result)
    
