from flask import jsonify
from .paymentMethodModel import db,PaymentMethod, PaymentMethodSchema

class PaymentMethodContoller:
    def insert(self):
        data=PaymentMethod(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=PaymentMethod.query.all()
        result=PaymentMethodSchema(many=True).dump(data)
        return jsonify(result)
    
