from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from utilidades import *

class Filme(db.Model):
    __tablename__ = "filmes"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    titulo = db.Column(db.String(255), nullable = False)
    genero = db.Column(db.String(100), nullable = False)
    ano_lancamento = db.Column(db.Integer, nullable = False)
    avaliacao = db.Column(db.Numeric(3, 1), nullable= False)


    __table_args__ = (
            CheckConstraint('avaliacao >= 0 AND avaliacao <= 10', name='check_avaliacao_range'),
        )