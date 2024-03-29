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
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def select_id(cls, id_entrada):
        return cls.query.filter.filter_by(id=id_entrada).first()
