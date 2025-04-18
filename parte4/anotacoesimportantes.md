## iniciando o flask 

<p>O flask é um microsserviço web que facilita a criação de aplicações web com python</p>

```python 
from flask import Flask 

app = Flask(__name__)
#criando uma rota por decorate 
#cada rota retorna uma página desejada
    @app.route("/")
    def index():
    return 'Index'

    if __name__ == '__main__':
    app.run()

```


### MVC 
<p>O flask se utiliza do modelo MVC para a construção das suas aplicações, com algumas particularidades, sendo divido em:</p>

- Models
- Controllers 
- Static: Onde ficam os templates em html, CSS e Javascript das páginas 

<p>O controle de rotas é feito no arquivo app.py e para acessar uma página fazemos o seguinte</p>

```python 
from flask import Flask 

app = Flask(__name__, static_folder=static)


    if __name__ == '__main__':
    app.run()

```


### Criando url's dinâmicas

- Porque urls dinâmicas?
    <p>Para fazer a chamada das páginas que queremos criar no nosso site e para conseguirmos passar algumas informações de uma página para outra e fazer essas integrações</p>

    <p>Para criar uma url dinâmica utillizamos tags html dentro das rotas para redirecionar as páginas</p>

```python 
from flask import Flask 

app = Flask(__name__)

#criando uma rota por decorate 
#cada rota retorna uma página desejada
@app.route("/hello")
@app.route("/hello/<nome>")
def hello(nome=''): #passamos nome como parametro
    return '<h1>Hello{}</h1>'.format(nome)


#criando o conceito de blogs 
#aqui criamos uma rota para o post de um blog de acordo com seu id, e caso não seja passado nenhum post retornamos o blog completo 

@app.route("/blog")
@app.route("/blog/<int:postID>")
def blog(postID=-1) :
    if postID >= 0:
        return "blog Info{}".format(postID)
    else :
        return 'Blog todo'


if __name__ == '__main__':
    app.run()

```

### Redirecionamento de url 

<p></p>

```python 
from flask import Flask, redirect, url_for

app = Flask(__name__)



if __name__ == '__main__':
    app.run()

```

### Migrações
<p>Migrações são o que permitem que o banco de dados esteja sempre atualizado, quando uma alterção
ocorrer no POSTGRESQL </p>