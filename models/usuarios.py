from flask_sqlalchemy import SQLAlchemy
from utilidades import *
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = ""
    cpf = db.Column(db.String(14), primary_key=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)  
    senha = db.Column(db.String(255), nullable=False) 

    def get_id(self):
        return self.cpf