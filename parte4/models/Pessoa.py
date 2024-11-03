# models/pessoa.py
from models.db import db

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    idpessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)


