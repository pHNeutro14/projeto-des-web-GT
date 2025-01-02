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

@app.route('/pesquisar_filme')
def pesquisar_filme():
    return render_template('pesquisar_filme.html')