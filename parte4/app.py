from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Pessoa, Hospedes
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL (substitua os valores entre <> pelos seus dados)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://gio:manaluiza1304@localhost/pousada'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'pousada'  # Defina uma chave secreta
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', )

@app.route('/cadastroHospede', methods=['GET'])
def cadastroHospede():
    return render_template('cadastroHospede.html',)


@app.route('/cadastrarHospede', methods=['POST'])
def cadastrarHospede():
     # Obter os dados do formulário
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    idpessoa = request.form.get('cpf')

    # Criar uma nova instância de Pessoa
    nova_pessoa = Pessoa(
        idpessoa=idpessoa,
        nome=nome,
        telefone=telefone,
        endereco=endereco,
    )

    # Adicionar a nova pessoa ao banco de dados
    db.session.add(nova_pessoa)
    db.session.commit()  # Commita para que a nova pessoa tenha um ID gerado

    # Criar uma nova instância de Hospedes usando o ID da nova pessoa
    novo_hospede = Hospedes(
        idpessoa=nova_pessoa.idpessoa # Usando o ID gerado da nova pessoa
    )

    # Adicionar ao banco de dados
    db.session.add(novo_hospede)
    db.session.commit()

    # Adicionar uma mensagem de sucesso
    flash('Hóspede cadastrado com sucesso!')

    # Redirecionar para a página de listagem ou a página inicial
    return redirect(url_for('cadastroHospede'))  # Ajuste para a rota corre


@app.route('/listarHospedes')
def listar_hospedes():
    hospedes = db.session.query(Pessoa.nome, Pessoa.telefone, Pessoa.endereco, Hospedes.idhospede).outerjoin(Hospedes).all()
    return render_template('listarHospedes.html', hospedes=hospedes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)


