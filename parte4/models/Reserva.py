# models/pessoa.py
from models.db import db
from datetime import date


class Reserva(db.Model):
    __tablename__ = 'reserva'
    idreserva = db.Column(db.Integer, primary_key=True)
    idhospede = db.Column(db.Integer, db.ForeignKey('hospede.idpessoa'), nullable=False)
    codquarto = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    datainicio = db.Column(db.Date, nullable=False)
    datafim = db.Column(db.Date, nullable=False)
    valordesconto = db.Column(db.Integer, default=date.today)
    hospede = db.relationship('Hospedes', backref='reserva')







