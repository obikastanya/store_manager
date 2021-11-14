from flask import jsonify
from application.master.stock.stockModel import Stock
from .stockModel import db,Stock, StockSchema

class StockController:
    def insert(self):
        data=Stock(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=Stock.query.all()
        result=StockSchema(many=True).dump(data)
        return jsonify(result)
    
