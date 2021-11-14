from .model import db, User, UserSchema
from flask import jsonify
class UserController:
    def insert(self):
        data=User(id=2, name='Yesa')
        db.session.add(data)
        db.session.commit()
        return 'sukses'
    def select(self):
        data=User.query.all()
        result=UserSchema(many=True).dump(data)
        return jsonify(result)
    
