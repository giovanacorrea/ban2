from flask import Flask 

app = Flask(__name__)

#criando uma rota por decorate 
#cada rota retorna uma página desejada
@app.route("/hello")
@app.route("/hello/<nome>")
def hello(nome=''): #passamos nome como parametro
    return '<h1>Hello{}</h1>'.format(nome)

@app.route("/blog")
@app.route("/blog/<int:postID>")
def blog(postID=-1) :
    if postID >= 0:
        return "blog Info{}".format(postID)
    else :
        return 'Blog todo'


if __name__ == '__main__':
    app.run(debug=True)
