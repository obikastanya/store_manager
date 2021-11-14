from flask import jsonify
from application.master.stock.stockModel import Stock
from .companyModel import db,Company, CompanySchema

class CompanyController:
    def insert(self):
        data=Company(mss_msp_id=1, mss_warehouse_stock=14, mss_store_stock=12)
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=Company.query.all()
        result=CompanySchema(many=True).dump(data)
        return jsonify(result)
    
