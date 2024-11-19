# models/hospede.py
from models.db import db
from models.Pessoa import Pessoa
from models.Hospedes import Hospedes

class Acompanhante(db.Model):
    __tablename__ = 'acompanhante'
    idacompanhante = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    idhospede = db.Column(db.Integer, db.ForeignKey('hospede.idhospede'), nullable=False)
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.idpessoa'), nullable=False)
    hospede = db.relationship('Hospedes', backref='acompanhante')
    pessoa = db.relationship('Pessoa', backref='acompanhante')
