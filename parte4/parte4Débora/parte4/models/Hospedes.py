# models/hospede.py
from models.db import db
from models.Pessoa import Pessoa

class Hospedes(db.Model):
    __tablename__ = 'hospede'
    idhospede = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.idpessoa'), nullable=False)
    pessoa = db.relationship('Pessoa', backref='hospede')
