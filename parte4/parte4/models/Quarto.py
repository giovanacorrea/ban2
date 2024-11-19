# models/quarto.py
from models.db import db

class Quarto(db.Model):
    __tablename__ = 'quarto'
    codquarto = db.Column(db.Integer, primary_key=True)
    tipo_quarto = db.Column(db.String(100), nullable=False)
    qtdcamas = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    frigobar = db.Column(db.String, nullable=False)
    banheira = db.Column(db.String, nullable=False)

