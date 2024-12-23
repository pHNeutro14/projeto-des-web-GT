from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adicionar_filme')
def adicionar_filme():
    return render_template('adicionar_filme.html')

@app.route('/excluir_filme')
def excluir_filme():
    return render_template('excluir_filme.html')

@app.route('pesquisar_filme')
def pesquisar_filme():
    return render_template('pesquisar_filme.html')