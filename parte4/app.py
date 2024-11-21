from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import InternalError
from models import db, Pessoa, Hospedes, Quarto, Reserva, Acompanhante, Consumo_frigobar
from flask_migrate import Migrate
import os

app = Flask(__name__)

ITENS_FRIGOBAR = ["água sem gás", "água com gás", "chocolate", "castanhas", "salgadinho"]
QUANTIDADE_INICIAL = 2

# Configuração do banco de dados PostgreSQL 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost/T2-BAN2'
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
    # Verifique os dados de entrada
    print("Dados recebidos do formulário:")
    print(request.form)

    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    idpessoa = request.form.get('cpf')

    # Cria a nova pessoa e adiciona ao banco
    nova_pessoa = Pessoa(idpessoa=idpessoa, nome=nome, telefone=telefone, endereco=endereco)
    db.session.add(nova_pessoa)
    db.session.commit()

    # Cria o novo hóspede e adiciona ao banco
    novo_hospede = Hospedes(idpessoa=nova_pessoa.idpessoa)
    db.session.add(novo_hospede)
    db.session.flush()

    # Verifique os acompanhantes
    nacompanhantes = request.form.getlist('acompanhante[]')
    print("Acompanhantes recebidos:", nacompanhantes)
    
    for nomeacompanhante in nacompanhantes:
        novo_acompanhante = Acompanhante(
            nome=nomeacompanhante,
            idhospede=novo_hospede.idhospede,
            idpessoa=nova_pessoa.idpessoa
        )
        db.session.add(novo_acompanhante)

    try:
        db.session.commit()
        flash('Hóspede e acompanhantes cadastrados com sucesso!')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao cadastrar: {str(e)}')
    
    return redirect(url_for('listar_hospedes'))


#Aqui está listando todas as pessoas e não apenas os hospedes, necessário corrigir 
@app.route('/listar_hospedes')
def listar_hospedes():
    hospedes = db.session.query(Pessoa.nome, Pessoa.telefone, Pessoa.endereco, Hospedes.idhospede).join(Hospedes, Pessoa.idpessoa == Hospedes.idpessoa).all()
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
    quartos = db.session.query(Quarto).all()
    print(quartos)
    return render_template('reserva.html', quartos=quartos)

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
        
    # Adicionar 2 unidades de cada item do frigobar para a nova reserva
    for item in ITENS_FRIGOBAR:
        consumo_inicial = Consumo_frigobar(
            idreserva=nova_reserva.idreserva,
            item=item,
            quantidade=QUANTIDADE_INICIAL,
            data=datainicio  # Data de entrada do hóspede
        )
        db.session.add(consumo_inicial)

    db.session.commit()  # Commit para salvar todos os registros de consumo inicial
        
    return redirect(url_for('reserva'))


@app.route('/listar_quartos')
def listar_quartos():
    quartos = db.session.query(Quarto.codquarto, Quarto.tipo_quarto, Quarto.qtdcamas, Quarto.preco)
    return render_template('listarQuartos.html', quartos=quartos)
  
@app.route('/relatorioReservasAtivas')
def relatorioReservasAtivas():
	reservas_ativas = db.session.query(Reserva, Hospedes, Pessoa, Quarto).join(Hospedes, Reserva.idhospede == Hospedes.idhospede).join(Pessoa, Hospedes.idpessoa == Pessoa.idpessoa).join(Quarto, Reserva.codquarto == Quarto.codquarto).filter(Reserva.estado == 'pago').all()
	return render_template('relatorioReservasAtivas.html', reservas_ativas=reservas_ativas)

@app.route('/relatorioReservasCanceladas')
def relatorioReservasCanceladas():
	reservas_canceladas = db.session.query(Reserva, Hospedes, Pessoa, Quarto).join(Hospedes, Reserva.idhospede == Hospedes.idhospede).join(Pessoa, Hospedes.idpessoa == Pessoa.idpessoa).join(Quarto, Reserva.codquarto == Quarto.codquarto).filter(Reserva.estado == 'naopago').all()	
	return render_template('relatorioReservasCanceladas.html', reservas_canceladas=reservas_canceladas)
	
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    reservas = None
    if request.method == 'POST':
        cpf = request.form.get('cpf')  # Obtém o CPF enviado pelo formulário
        # Consulta para encontrar reservas pelo CPF
        reservas = db.session.query(Reserva, Hospedes, Pessoa)\
            .join(Hospedes, Hospedes.idhospede == Reserva.idhospede)\
            .join(Pessoa, Hospedes.idpessoa == Pessoa.idpessoa)\
            .filter(Pessoa.idpessoa == cpf)\
            .all()
        
        if not reservas:
            flash("Nenhuma reserva encontrada para o CPF fornecido.")
    
    return render_template('checkout.html', reservas=reservas)

from flask import render_template, request, flash, redirect, url_for
from datetime import date

@app.route('/checkout2/<int:idreserva>', methods=['GET', 'POST'])
def checkout2(idreserva):
    # Consulta para buscar os detalhes da reserva pelo ID
    reserva_info = db.session.query(Reserva, Hospedes, Pessoa, Quarto)\
        .join(Hospedes, Hospedes.idhospede == Reserva.idhospede)\
        .join(Pessoa, Hospedes.idpessoa == Pessoa.idpessoa)\
        .join(Quarto, Reserva.codquarto == Quarto.codquarto)\
        .filter(Reserva.idreserva == idreserva)\
        .first()

    # Verificação para garantir que a reserva foi encontrada
    if not reserva_info:
        flash("Reserva não encontrada.")
        return redirect(url_for('checkout'))

    # Processamento dos dados do formulário (POST)
    if request.method == 'POST':
        # Obter as quantidades informadas no formulário
        consumo_itens = {
            "água sem gás": request.form.get('aguasgas', type=int),
            "água com gás": request.form.get('aguacgas', type=int),
            "chocolate": request.form.get('chocolate', type=int),
            "castanhas": request.form.get('castanhas', type=int),
            "salgadinho": request.form.get('salgadinho', type=int)
        }

        # Iterar sobre os itens consumidos e registrar no banco de dados
        for item, quantidade in consumo_itens.items():
            if quantidade > 0:  # Registrar apenas itens com quantidade maior que zero
                novo_consumo = Consumo_frigobar(
                    idreserva=idreserva,
                    item=item,
                    quantidade=quantidade,
                    data=date.today()
                )
                db.session.add(novo_consumo)

        # Commit para salvar os dados no banco de dados
        db.session.commit()
        flash('Consumo de frigobar registrado com sucesso!')

        # Redireciona para evitar reenvio do formulário
        return redirect(url_for('checkout2', idreserva=idreserva))

    return render_template('checkout2.html', reserva_info=reserva_info)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
