from flask import jsonify
from .productModel import db,Product, ProductSchema

class ProductController:
    def insert(self):
        data=Product(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=Product.query.all()
        result=ProductSchema(many=True).dump(data)
        return jsonify(result)
    
