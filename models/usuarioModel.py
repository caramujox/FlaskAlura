from db import db


class Usuario(db.Model):
    def __init__(self, id, nome, senha, user):
        self.id = id
        self.nome = nome
        self.user = user
        self.senha = senha