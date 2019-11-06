from db import db

class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable = False)
    console = db.Column(db.String(200), nullable = False)



    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

def toDict(self):
    return {'nome': self.nome, 'categoria': self.categoria, 'console': self.console}
