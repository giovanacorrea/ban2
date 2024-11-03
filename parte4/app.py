from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Pessoa, Hospedes
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL (substitua os valores entre <> pelos seus dados)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://gio:manaluiza1304@localhost/pousada'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', )

@app.route('/cadastrarHospede', methods=['GET', 'POST'])
def cadastrarHospede():
    return render_template('cadastrarHospede.html')


@app.route('/listarHospedes')
def listar_hospedes():
    hospedes = db.session.query(Pessoa.nome, Pessoa.telefone, Pessoa.endereco, Hospedes.idhospede).join(Hospedes).all()
    return render_template('listar_hospedes.html', hospedes=hospedes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)


