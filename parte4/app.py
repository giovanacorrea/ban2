from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import InternalError
from models import db, Pessoa, Hospedes, Quarto, Reserva
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost/T2-BAN2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://gio:manaluiza1304@localhost/pousada'

# Configuração do banco de dados PostgreSQL (substitua os valores entre <> pelos seus dados)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://gio:manaluiza1304@localhost/pousada'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'pousada'  # Defina uma chave secreta
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/index')
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

#Aqui está listando todas as pessoas e não apenas os hospedes, necessário corrigir 
@app.route('/listar_hospedes')
def listar_hospedes():
    hospedes = db.session.query(Pessoa.nome, Pessoa.telefone, Pessoa.endereco, Hospedes.idhospede).outerjoin(Hospedes).all()
    return render_template('listarHospedes.html', hospedes=hospedes)

@app.route('/cadastrarQuarto')
def cadastrarQuarto():
    return render_template('cadastrarQuarto.html')

@app.route('/cadastroQuarto', methods=['POST'])
def cadastroQuarto():
    # Obter os dados do formulário
    codquarto = request.form.get('numquarto')  
    tipo_quarto = request.form.get('tipoQuarto')
    qtdcamas = request.form.get('quantidadeCamas')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')
    frigobar = request.form.get('frigobar')
    banheira = request.form.get('banheira')
    
    # Criar uma nova instância de Quarto
    novo_quarto = Quarto(
        codquarto=codquarto,
        tipo_quarto=tipo_quarto,
        qtdcamas=qtdcamas,
        preco=preco,
        descricao=descricao,
        frigobar=frigobar,
        banheira=banheira
    )
    
    # Adicionar o novo quarto ao banco de dados
    db.session.add(novo_quarto)
    db.session.commit()

    # Adicionar uma mensagem de sucesso
    flash('Quarto cadastrado com sucesso!')

    # Redirecionar para a página de listagem ou a página inicial
    return redirect(url_for('cadastrarQuarto'))
    
@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/CadastrarReserva',  methods=['POST'])
def CadastrarReserva():
    idhospede = request.form.get('cpf')
    codquarto = request.form.get('numquarto')
    estado = request.form.get('estado')
    datainicio = request.form.get('datainicio')
    datafim = request.form.get('datafim')
    valordesconto = request.form.get('cupom')

    subconsulta_idhospede = db.session.query(Hospedes.idhospede).join(Pessoa).filter(Pessoa.idpessoa == idhospede).scalar_subquery()

    # Verificação para garantir que o idhospede foi encontrado antes de continuar
    if subconsulta_idhospede is None:
        flash('Hospede com o CPF informado não encontrado!')
        return redirect(url_for('formulario_cadastro_reserva'))
    
    # Criar uma nova instância de Quarto
    nova_reserva = Reserva(
        idhospede= subconsulta_idhospede,
        codquarto=codquarto,
        estado=estado,
        datainicio=datainicio,
        datafim=datafim,
        valordesconto=valordesconto
    )
    
    try:
        # Adicionar e salvar a nova reserva no banco de dados
        db.session.add(nova_reserva)
        db.session.commit()
        flash('Reserva cadastrada com sucesso!')
        return redirect(url_for('reserva'))
    except InternalError as e:
        # Desfazer a transação caso ocorra um erro
        db.session.rollback()
        
        # Verificar a mensagem de erro e exibir um alerta específico
        if "O quarto" in str(e.orig):
            flash(str(e.orig).split('\n')[0])  # Exibe apenas a primeira linha do erro
        else:
            flash('Ocorreu um erro ao cadastrar a reserva. Tente novamente.')
        
        return redirect(url_for('reserva'))


@app.route('/listar_quartos')
def listar_quartos():
    quartos = db.session.query(Quarto.codquarto, Quarto.tipo_quarto, Quarto.qtdcamas, Quarto.preco)
    return render_template('listarQuartos.html', quartos=quartos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)


