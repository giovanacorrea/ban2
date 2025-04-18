from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'  

MONGO_URI = "mongodb+srv://debora:debora@cluster0.ryu6t.mongodb.net/pousada?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['pousada']

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
    acompanhantes = request.form.getlist('acompanhante[]')  


    if not all([cpf, nome, telefone, endereco]):
        flash("Todos os campos são obrigatórios!")
        return redirect(url_for('cadastroHospede'))

    try:
        db.hospedes.insert_one({
            "cpf": cpf,
            "nome": nome,
            "telefone": telefone,
            "endereco": endereco
        })
        for acompanhante in acompanhantes:
            print(acompanhante)
            db.acompanhantes.insert_one({
                "nome": acompanhante,
                "hospede_id": cpf  
            })

        flash('Hóspede e acompanhantes cadastrados com sucesso!')
    except Exception as e:
        flash(f"Erro ao cadastrar hóspede e acompanhantes: {e}")

    return redirect(url_for('listar_hospedes'))



@app.route('/listar_hospedes')
def listar_hospedes():
    try:
        hospedes = db.hospedes.find()
        return render_template('listarHospedes.html', hospedes=hospedes)
    except Exception as e:
        flash(f"Erro ao listar hóspedes: {e}")
        return redirect(url_for('index'))

@app.route('/cadastrarQuarto')
def cadastrarQuarto():
    return render_template('cadastrarQuarto.html')

@app.route('/cadastroQuarto', methods=['POST'])
def cadastroQuarto():
    numquarto = request.form.get('numquarto')  
    tipo_quarto = request.form.get('tipoQuarto')
    qtdcamas = request.form.get('quantidadeCamas')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')

    try:
        db.quartos.insert_one({
            "numquarto": numquarto,
            "tipo_quarto": tipo_quarto,
            "quantidade_camas": qtdcamas,
            "preco": preco,
            "descricao": descricao
        })
        flash('Quarto cadastrado com sucesso!')
    except Exception as e:
        flash(f"Erro ao cadastrar quarto: {e}")

    return redirect(url_for('cadastrarQuarto'))
    
@app.route('/listar_quartos')
def listar_quartos():
    try:
        quartos = db.quartos.find()
        return render_template('listarQuartos.html', quartos=quartos)
    except Exception as e:
        flash(f"Erro ao listar quartos: {e}")
        return redirect(url_for('index'))

@app.route('/reserva')
def reserva():
    try:
        quartos = db.quartos.find()
        return render_template('reserva.html', quartos=quartos)
    except Exception as e:
        flash(f"Erro ao buscar quartos: {e}")
        return redirect(url_for('index'))

@app.route('/CadastrarReserva', methods=['POST'])
def CadastrarReserva():
    cpf = request.form.get('cpf')
    numquarto = request.form.get('numquarto')
    estado = request.form.get('estado')
    datainicio = request.form.get('datainicio')
    datafim = request.form.get('datafim')
    valordesconto = request.form.get('cupom')

    try:
        reserva_existente = db.reservas.find_one({
            "numquarto": numquarto,
            "$or": [
                {"datainicio": {"$lte": datafim}, "datafim": {"$gte": datainicio}},
            ]
        })

        if reserva_existente:
            flash('Este quarto já está reservado para esse período.')
            return redirect(url_for('reserva'))

        db.reservas.insert_one({
            "cpf_hospede": cpf,
            "numquarto": numquarto,
            "estado": estado,
            "datainicio": datainicio,
            "datafim": datafim,
            "valordesconto": valordesconto
        })
        flash('Reserva cadastrada com sucesso!')
    except Exception as e:
        flash(f"Erro ao cadastrar reserva: {e}")

    return redirect(url_for('reserva'))


@app.route('/relatorioReservasAtivas')
def relatorioReservasAtivas():
    try:
        reservas_ativas = db.reservas.aggregate([
            {
                '$match': {
                    'estado': 'pago'  
                }
            },
            {
                '$lookup': {
                    'from': 'hospedes',  
                    'localField': 'cpf_hospede',  
                    'foreignField': 'cpf',  
                    'as': 'hospede_info'  
                }
            }
        ])
        
        return render_template('relatorioReservasAtivas.html', reservas_ativas=reservas_ativas)
    except Exception as e:
        flash(f"Erro ao buscar reservas ativas: {e}")
        return redirect(url_for('index'))


@app.route('/relatorioReservasCanceladas')
def relatorioReservasCanceladas():
    try:
        reservas_canceladas = db.reservas.aggregate([
            {
                '$match': {
                    'estado': 'naopago'  
                }
            },
            {
                '$lookup': {
                    'from': 'hospedes',  
                    'localField': 'cpf_hospede',  
                    'foreignField': 'cpf',  
                    'as': 'hospede_info' 
                }
            }
        ])
        
        return render_template('relatorioReservasCanceladas.html', reservas_canceladas=reservas_canceladas)
    except Exception as e:
        flash(f"Erro ao buscar reservas canceladas: {e}")
        return redirect(url_for('index'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    reservas = None
    cpf = None 
    hospedes = None
    if request.method == 'POST':
        cpf = request.form.get('cpf', '').strip()  

        print(f"Consultando CPF: {cpf}")
        print(f"Consultando CPF: {reservas}")
        reservas = list(db.reservas.find({"cpf_hospede": cpf})) 
        hospedes = list(db.hospedes.find({"cpf": cpf})) 

        print(f"Reservas encontradas: {reservas}")
        print(f"Hospedes encontradas: {hospedes}")


        if not reservas:
            flash("Nenhuma reserva encontrada para o CPF fornecido.")
    
    return render_template('checkout.html', reservas=reservas, hospedes=hospedes)


@app.route('/checkout2/<string:idreserva>', methods=['GET', 'POST'])
def checkout2(idreserva):
    try:
        reserva_info = db.reservas.find_one({"_id": ObjectId(idreserva)}) 
        cpf_hospede = reserva_info.get("cpf_hospede") 
        codquarto = reserva_info.get("codquarto")  
        quarto_info = db.quartos.find_one({"codquarto": codquarto})
        
        
        hospedes_info = db.hospedes.find_one({"cpf": cpf_hospede})
        print(f"Reserva encontrada: {reserva_info}")
        print(f"Hóspede encontrado: {hospedes_info}")
        print(f"Quarto encontrado: {quarto_info}")


    except Exception as e:
        flash(f"Erro ao procurar reserva: {str(e)}")
        return redirect(url_for('checkout'))

    if not reserva_info:
        flash("Reserva não encontrada.")
        return redirect(url_for('checkout'))

    if request.method == 'POST':
        try:
            consumo_itens = {
                "água sem gás": request.form.get('aguasgas', type=int),
                "água com gás": request.form.get('aguacgas', type=int),
                "chocolate": request.form.get('chocolate', type=int),
                "castanhas": request.form.get('castanhas', type=int),
                "salgadinho": request.form.get('salgadinho', type=int)
            }

            itens_consumidos = [
                {"item": item, "quantidade": quantidade, "data": date.today().strftime("%Y-%m-%d") , "numquarto": quarto_info["numquarto"]}
                for item, quantidade in consumo_itens.items() if quantidade > 0
            ]

            if itens_consumidos:
                db.consumo_frigobar.insert_many(itens_consumidos)
                flash("Consumo registrado com sucesso!")
            else:
                flash("Nenhum item consumido foi registrado.")

        except Exception as e:
            flash(f"Erro ao registrar consumo: {str(e)}")
            return redirect(url_for('checkout2', idreserva=idreserva))

        
        flash('Consumo registrado com sucesso!')
        return redirect(url_for('checkout2', idreserva=idreserva))

    return render_template('checkout2.html', reserva_info=reserva_info, hospedes_info=hospedes_info, quarto_info=quarto_info)


if __name__ == '__main__':
    app.run(debug=True)