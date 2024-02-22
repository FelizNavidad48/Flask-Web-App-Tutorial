from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    patvirtinta = db.Column(db.Boolean, default=False)

    user_darbuotojas_id = db.relationship('Darbuotojas')


# Darbuotojas
class Darbuotojas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ataskaitos = db.relationship('DienosAtaskaita')
    # Kai ikainiu nera dabartinis_ikainis == null
    dabartinis_ikainis = db.Column(db.Float, db.ForeignKey('ikainis.id'))


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
    deziu_kiekis = db.Column(db.Integer)
    darbuotojai = db.relationship('Darbuotojas')
