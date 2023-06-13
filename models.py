""" This is the models module
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, String, Text,func,Boolean, Enum
from sqlalchemy.schema import FetchedValue
from datetime import datetime
import enum
from sqlalchemy.sql import func

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apidatabase.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class State(db.Model):
    __tablename__ = 'state'

    id_no = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(50), nullable=False)
    capital = db.Column(db.String(50), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    created = db.Column(db.Integer, nullable=True) #year of creation
    landmass = db.Column(db.Integer, nullable=True)
    reg = db.Column(db.DateTime, default=func.now())
    linklga = db.relationship('LocalGovt', backref='state', lazy='dynamic')
    linklocation = db.relationship('Location', backref='state', lazy='dynamic')
    linkstreet = db.relationship('Street', backref='state', lazy='dynamic')
    def __repr__(self):
        return self.state

class LocalGovt(db.Model):
    __tablename__ = 'local_govt'

    id_no = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id_no'))
    local_govt = db.Column(db.String(50),server_default=db.FetchedValue())
    population = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime(), nullable=True)
    landmass = db.Column(db.Integer, nullable=True)
    reg = db.Column(db.DateTime, default=func.now())    
    linklocation = db.relationship('Location', backref='local_govt', lazy='dynamic')
    linkstreet = db.relationship('Street', backref='local_govt', lazy='dynamic')
    
    def __repr__(self):
        return self.local_govt 

class Location(db.Model):
    __tablename__ = 'land_marks'

    loc_id = db.Column(db.Integer, primary_key=True)
    stateID = db.Column(db.Integer, db.ForeignKey('state.id_no'))
    lgaID = db.Column(db.Integer, db.ForeignKey('local_govt.id_no'))
    location = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=True)
    reg = db.Column(db.DateTime, default=func.now())    
    linkstreet = db.relationship('Street', backref='land_marks', lazy='dynamic')

    def __repr__(self):
        return self.location

class Street(db.Model):
    __tablename__ = 'streets'

    strid = db.Column(db.Integer, primary_key=True)
    stateID = db.Column(db.Integer, db.ForeignKey('state.id_no'))
    lgaID = db.Column(db.Integer, db.ForeignKey('local_govt.id_no'))
    locID = db.Column(db.Integer, db.ForeignKey('land_marks.loc_id'))
    streetname = db.Column(db.String(50), nullable=False)
    reg = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return self.streetname  
