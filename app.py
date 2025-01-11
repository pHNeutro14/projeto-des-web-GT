from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from models.model_db import *
from models.usuarios import *
from utilidades import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
load_dotenv()

dbusuario = os.getenv("DB_USERNAME")
dbsenha = os.getenv("DB_PASSWORD") 
host = os.getenv("DB_HOST") 
meubanco = os.getenv("DB_DATABASE") 
porta = os.getenv("DB_PORT")
conexao = f"mysql+pymysql://{dbusuario}:{dbsenha}@{host}:{porta}/{meubanco}"
app.config["SQLALCHEMY_DATABASE_URI"] = conexao 
db.init_app(app) 
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
lm.init_app(app)

@lm.user_loader
def load_user(cpf):
    return Usuario.query.get(cpf) 

@app.route('/', methods = ["get", "post"])
def index():
    return render_template('index.html')

@app.route('/adicionar_filme', methods = ["get", "post"])
def adicionar_filme():
    return render_template('adicionar_filme.html')

@app.route('/enviar_filme', methods = ["get", "post"])
def enviar_filme():
    titulo = request.form.get('titulo')
    genero = request.form.get('genero')
    ano_lancamento = request.form.get('ano_lancamento')
    avaliacao = request.form.get('avaliacao')
    novo_filme = Filme(titulo = titulo, genero = genero, ano_lancamento = ano_lancamento, avaliacao = avaliacao)
    db.session.add(novo_filme)
    db.session.commit()
    return render_template('enviar_filme.html', titulo = titulo, genero = genero, ano_lancamento = ano_lancamento, avaliacao = avaliacao)

@app.route('/excluir_filme', methods = ["get", "post"])
def excluir_filme():
    return render_template('excluir_filme.html')

@app.route('/filme_excluido', methods = ["get", "post"])
def filme_excluido():
    filme_id = request.form.get('id')

    if not filme_id:
        mensagem_excluir = "Não foi encontrado nenhum filme com esse id"
        return render_template('filme_excluido.html', mensagem_excluir=mensagem_excluir)
    
    excluir_filme = Filme.query.get(filme_id)
    if excluir_filme:
        db.session.delete(excluir_filme)
        db.session.commit()
        mensagem_excluir = "Filme excluido!"

    else:
        mensagem_excluir = "Não foi encontrado nenhum filme com esse id"

    return render_template('filme_excluido.html', mensagem_excluir=mensagem_excluir)

@app.route('/pesquisar_filme', methods = ["get", "post"])
def pesquisar_filme():
    return render_template('pesquisar_filme.html')

@app.route('/exibir_filme', methods = ["get", "post"])
def exibir_filme():
    titulo = request.form.get('titulo')
    if not titulo:
        filmes = Filme.query.all()
    else:
        filmes = Filme.query.filter_by(titulo=titulo).all()  

    return render_template('exibir_filme.html', filmes=filmes, titulo=titulo)

@app.route('/editar_avaliacao', methods = ["get", "post"])
def editar_avaliacao():
    return render_template('editar_avaliacao.html')

@app.route('/filme_editado', methods = ["get", "post"])
def filme_editado():
    filme_id = request.form.get('id')
    nova_avaliacao = request.form.get('avaliacao')
    filme = Filme.query.get(filme_id)
    filme.avaliacao = nova_avaliacao
    db.session.commit()
    return render_template('filme_editado.html', filme = filme)

@app.route('/cadastro', methods = ["get", "post"])
def cadastro():
    return render_template('cadastro.html')

@app.route("/cadastrar_usuario", methods = ["get", "post"])
def cadastrar_usuario():
    if request.method == "POST":
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        if not cpf or not nome or not senha:
            mensagem = "Todos os campos são obrigatórios."
            return render_template("cadastrar_usuario.html", mensagem=mensagem)

        try:
            novo_usuario = Usuario(cpf=cpf, nome=nome, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()
            mensagem = "Usuário cadastrado com sucesso!"
        except Exception as e:
            db.session.rollback()
            mensagem = f"Erro ao cadastrar usuário: {e}"

        return render_template("cadastrar_usuario.html", mensagem=mensagem)

@app.route('/login', methods = ["post", "get"])
def login():
    return render_template("login.html")


@app.route('/usuario_logado', methods = ["post", "get"])
def usuario_logado():
    cpf = request.form.get('cpf')
    senha = request.form.get('senha')
    usuario = Usuario.query.filter_by(cpf=cpf).first()


    if usuario.cpf == cpf and usuario.senha == senha:
        login_user(usuario) 
        return render_template("usuario_logado.html", usuario = usuario)
    
    else: 
        mensagem = "credenciais não encontradas"
        return render_template("login.html", mensagem = mensagem)
    
@app.route('/logout', methods = ["get", "post"])
@login_required 
def logout():
    logout_user()
    return render_template("login.html") 

@app.errorhandler(404)
def erro404(error):
    return render_template('404.html'), 404

@app.errorhandler(401)
def erro401(error):
    return render_template('401.html'), 401