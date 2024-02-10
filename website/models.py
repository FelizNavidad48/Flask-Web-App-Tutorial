from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    role = db.Column(db.String(150))

    user_darbuotojas_id = db.relationship('Darbuotojas')


# Darbuotojas
class Darbuotojas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ataskaitos = db.relationship('DienosAtaskaita')


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
