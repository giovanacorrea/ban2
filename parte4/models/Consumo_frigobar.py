# models/consumo_frigobar.py
from models.db import db
from datetime import date


class Consumo_frigobar(db.Model):
    __tablename__ = 'consumo_frigobar'
    idconsumo = db.Column(db.Integer, primary_key=True)
    idreserva = db.Column(db.Integer, db.ForeignKey('reserva.idreserva'), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Date, nullable=False)
    
    