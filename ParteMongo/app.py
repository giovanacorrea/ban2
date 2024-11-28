from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'  # Chave para mensagens flash

# Configuração do MongoDB
app.config["MONGO_URI"] = "mongodb+srv://debora:debora@cluster0.ryu6t.mongodb.net/"
mongo = PyMongo(app)

# Itens do frigobar e quantidade inicial
ITENS_FRIGOBAR = ["água sem gás", "água com gás", "chocolate", "castanhas", "salgadinho"]
QUANTIDADE_INICIAL = 2
    
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/cadastroHospede', methods=['GET'])
def cadastroHospede():
    return render_template('cadastroHospede.html')
    
@app.route('/cadastrarHospede', methods=['POST'])
def cadastrarHospede():
    cpf = request.form.get('cpf')
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')

    # Inserir o hóspede no banco de dados MongoDB
    mongo.db.hospede.insert_one({
        "cpf": cpf,
        "nome": nome,
        "telefone": telefone,
        "endereco": endereco
    })

    flash('Hóspede cadastrado com sucesso!')
    return redirect(url_for('listar_hospedes'))


@app.route('/listar_hospedes')
def listar_hospedes():
    hospedes = []  # Aqui seria feita a consulta no banco
    return render_template('listarHospedes.html', hospedes=hospedes)

@app.route('/cadastrarQuarto')
def cadastrarQuarto():
    return render_template('cadastrarQuarto.html')

@app.route('/cadastroQuarto', methods=['POST'])
def cadastroQuarto():
    codquarto = request.form.get('numquarto')  
    tipo_quarto = request.form.get('tipoQuarto')
    qtdcamas = request.form.get('quantidadeCamas')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')
    flash('Quarto cadastrado com sucesso!')
    return redirect(url_for('cadastrarQuarto'))

@app.route('/reserva')
def reserva():
    quartos = []  # Aqui seria feita a consulta no banco
    return render_template('reserva.html', quartos=quartos)

@app.route('/CadastrarReserva', methods=['POST'])
def CadastrarReserva():
    idhospede = request.form.get('cpf')
    codquarto = request.form.get('numquarto')
    estado = request.form.get('estado')
    datainicio = request.form.get('datainicio')
    datafim = request.form.get('datafim')
    valordesconto = request.form.get('cupom')
    flash('Reserva cadastrada com sucesso!')
    return redirect(url_for('reserva'))

@app.route('/listar_quartos')
def listar_quartos():
    quartos = []  # Aqui seria feita a consulta no banco
    return render_template('listarQuartos.html', quartos=quartos)

@app.route('/relatorioReservasAtivas')
def relatorioReservasAtivas():
    reservas_ativas = []  # Aqui seria feita a consulta no banco
    return render_template('relatorioReservasAtivas.html', reservas_ativas=reservas_ativas)

@app.route('/relatorioReservasCanceladas')
def relatorioReservasCanceladas():
    reservas_canceladas = []  # Aqui seria feita a consulta no banco
    return render_template('relatorioReservasCanceladas.html', reservas_canceladas=reservas_canceladas)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    reservas = None
    if request.method == 'POST':
        cpf = request.form.get('cpf')  
        reservas = []  # Aqui seria feita a consulta no banco
        if not reservas:
            flash("Nenhuma reserva encontrada para o CPF fornecido.")
    return render_template('checkout.html', reservas=reservas)

@app.route('/checkout2/<int:idreserva>', methods=['GET', 'POST'])
def checkout2(idreserva):
    reserva_info = {}  # Aqui seria feita a consulta no banco
    if not reserva_info:
        flash("Reserva não encontrada.")
        return redirect(url_for('checkout'))

    if request.method == 'POST':
        consumo_itens = {
            "água sem gás": request.form.get('aguasgas', type=int),
            "água com gás": request.form.get('aguacgas', type=int),
            "chocolate": request.form.get('chocolate', type=int),
            "castanhas": request.form.get('castanhas', type=int),
            "salgadinho": request.form.get('salgadinho', type=int)
        }
        flash('Consumo de frigobar registrado com sucesso!')
        return redirect(url_for('checkout2', idreserva=idreserva))

    return render_template('checkout2.html', reserva_info=reserva_info)

if __name__ == '__main__':
    app.run(debug=True)

