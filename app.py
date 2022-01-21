from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
POSTGRES={
    'user':'postgres',
    'pw':'root',
    'db':'store_management',
    'host':'localhost',
    'port':'5432'
}


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s'%POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db= SQLAlchemy(app)
migrate=Migrate(app,db)

