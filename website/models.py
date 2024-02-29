from . import db
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy.sql import func


class User(db.Model, UserMixin, Base):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    patvirtinta = db.Column(db.Boolean, default=False)

    user_darbuotojas_id = db.relationship('Darbuotojas')


# Association Table
ikainis_darbuotojas_asociacija = Table(
    'ikainis_darbuotojas_asociacija', db.Model.metadata,
    Column('ikainio_id', db.Integer, ForeignKey('ikainis.id')),
    Column('darbuotojo_id', db.Integer, ForeignKey('darbuotojas.id')),

)


# Darbuotojas
class Darbuotojas(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    ataskaitos = db.relationship('DienosAtaskaita')
    ikainiai = db.relationship('Ikainis', secondary='ikainis_darbuotojas_asociacija', back_populates='darbuotojai')


# Darbuotojo dienos ataskaita
class DienosAtaskaita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    darbuotojo_id = db.Column(db.Integer, db.ForeignKey('darbuotojas.id'))
    data = db.Column(db.String(10))
    perkeltos_dezes = db.Column(db.Integer)
    atidirbtos_valandos = db.Column(db.Float)
    atlygis = db.Column(db.Float, default=0.0)
    patvirtinta = db.Column(db.Boolean, default=False)


# Vadybininkas
class Vadybininkas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Ikainis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10))
    valandinis = db.Column(db.Float)
    atlygis_uz_deze = db.Column(db.Integer)
    darbuotojai = db.relationship('Darbuotojas', secondary='ikainis_darbuotojas_asociacija', back_populates='ikainiai')
