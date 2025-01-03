from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from models.model_db import *

from utilidades import *

app = Flask(__name__)
load_dotenv()

dbusuario = os.getenv("DB_USERNAME")
dbsenha = os.getenv("DB_PASSWORD") 
host = os.getenv("DB_HOST") 
meubanco = os.getenv("DB_DATABASE") 

conexao = f"mysql+pymysql://{dbusuario}:{dbsenha}@{host}/{meubanco}" 
app.config["SQLALCHEMY_DATABASE_URI"] = conexao 
db.init_app(app) 

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