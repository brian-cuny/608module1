from . import db
from datetime import datetime
from sqlalchemy.orm import backref
from flask import current_app
from sqlalchemy.sql.expression import or_, desc


class States(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.INTEGER, primary_key=True)
    state = db.Column(db.String(40), unique=True)
    abbreviation = db.Column(db.String(3), unique=True)


class Counties(db.Model):
    __tablename__ = 'counties'
    id = db.Column(db.INTEGER, primary_key=True)
    county = db.Column(db.String(100))
    state_id = db.Column(db.INTEGER, db.ForeignKey('states.id'))

    state = db.relationship('States', backref=backref('county_list', lazy='dynamic'))


class Metros(db.Model):
    __tablename__ = 'metros'
    id = db.Column(db.INTEGER, primary_key=True)
    metro = db.Column(db.String(100), unique=True)


class Populations(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    county_id = db.Column(db.INTEGER, db.ForeignKey('counties.id'))
    year = db.Column(db.DATE)
    population = db.Column(db.INTEGER)

    county = db.relationship('Counties', backref=backref('population_list', lazy='dynamic'))


class Metros_Counties(db.Model):
    __tablename__ = 'metros_counties'
    id = db.Column(db.INTEGER, primary_key=True)
    metro_id = db.Column(db.INTEGER, db.ForeignKey('metros.id'))
    county_id = db.Column(db.INTEGER, db.ForeignKey('counties.id'))

    metro = db.relationship('Metros', backref=backref('county_list', lazy='dynamic'))
    county = db.relationship('Counties', backref=backref('metro_list', lazy='dynamic'))
