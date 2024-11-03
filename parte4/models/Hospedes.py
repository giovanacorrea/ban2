# models/hospede.py
from models.db import db
from models.Pessoa import Pessoa

class Hospede(db.Model):
    __tablename__ = 'hospedes'
    idhospede = db.Column(db.Integer, primary_key=True)
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.idpessoa'), nullable=False)
    pessoa = db.relationship('Pessoa', backref='hospede')
