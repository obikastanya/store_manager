from flask import jsonify
from .categoryProductModel import db,CategoryProductSchema, CategoryProduct

class CategoryProductController:
    def insert(self):
        data=CategoryProduct(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=CategoryProduct.query.all()
        result=CategoryProductSchema(many=True).dump(data)
        return jsonify(result)
    
