from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', )

@app.route('/cadastrarHospede', methods=['GET', 'POST'])
def cadastrarHospede():
    return render_template('cadastrarHospede.html')


# @app.route('/listarHospedes')
# def listarHospedes():
#     return render_template('listarHospedes.html')

if __name__ == '__main__':
    app.run(debug=True)


#criando uma rota por decorate 
#cada rota retorna uma página desejada
# @app.route("/hello")
# @app.route("/hello/<nome>")
# def hello(nome=''): #passamos nome como parametro
#     return '<h1>Hello{}</h1>'.format(nome)

# @app.route("/blog")
# @app.route("/blog/<int:postID>")
# def blog(postID=-1) :
#     if postID >= 0:
#         return "blog Info{}".format(postID)
#     else :
#         return 'Blog todo'
