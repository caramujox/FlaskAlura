from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_restful import Resource, Api
from db import db
import os

app = Flask(__name__)
app.secret_key = 'caiao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
app.config['SQLALCHEMY_BINDS'] = {
    'jogos': 'sqlite:///jogo.db',
    'user': 'sqlite:///user.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
# @app.route("/")
# def hello():
#     return "HelloWorld!"

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Jogo(db.Model):
    __bind_key__ = 'jogos'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(200), nullable = False)
    categoria = db.Column(db.String(200), nullable = False)
    console = db.Column(db.String(200), nullable = False)


    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario(db.Model):
    __bind_key__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(2000), nullable = False)
    email = db.Column(db.String(2000), nullable = False)
    senha = db.Column(db.String(2000), nullable = False)
    username = db.Column(db.String(2000), nullable = False)

    def __init__(self, username, nome, senha, email):
        self.username = username
        self.nome = nome
        self.email = email
        self.senha = senha


#inserir usuarios na mao
usuario1 = Usuario('luan', 'Luan Marques', '1234', 'luan')
usuario2 = Usuario('2', 'Caio', '3540', 'caiao')
usuario3 = Usuario('3', 'Carol', '9876', 'carol')

#inserir jogos na mao
jogo1 = Jogo('Super Mario', 'Acao', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
     


@app.route('/')
def index():
    lista = Jogo.query.all()
    return render_template('lista.html', titulo = 'Jogos', jogos = lista)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('cadastro')))
    return render_template('cadastro.html', titulo = 'Cadastre o seu novo Jogo')

@app.route('/criar_jogo', methods = ['POST',])
def criar_jogo():
    uploadPath=app.config['UPLOAD_PATH']
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)    
    db.session.add(jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    arquivo.save(f'{uploadPath}/capa{jogo.id}.jpg')


    #lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/cadastrousuario')
def cadastroUsuario():
    return render_template('cadastrousuario.html', titulo = 'Cadastre-se!')

@app.route('/criar_usuario', methods=['POST',])
def criar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    username = request.form['username']
    senha = request.form['senha']
    user = Usuario(nome, email, username, senha)
    
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))   

@app.route('/listar_usuarios', methods=['GET',])
def listaUser():
    lista = Usuario.query.all()
    return render_template('listausuario.html', titulo = 'Usuarios', usuarios = lista)

    
@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuarios = Usuario.query.all() 
    if request.form['usuario'] in usuarios:
        user = usuarios[request.form['usuario']]        
        if user.senha == request.form['senha']:
            session['usuario_logado'] = user.username
            flash(user.nome + ' logado')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Senha errada!')
            return redirect(url_for('login'))        
    else:
        flash('Usuário não cadastrado, favor realizar o cadastro!')
        return redirect(url_for('login'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('editar')))
    jogo = Jogo.query.filter_by(id=id).first()
    return render_template('editar.html', titulo = 'Edite seu Jogo', jogo = jogo, capa_jogo = f'capa{id}.jpg')

@app.route('/atualizar', methods = ['POST',])
def atualizar():    

    idform = request.form['id']
    jogo = Jogo.query.filter_by(id = idform).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']    
    db.session.commit()

    #lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/deletar/<int:id_jogo>')
def deletar(id_jogo):
    jogo = Jogo.query.filter_by(id=id_jogo).first()
    db.session.delete(jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('None user logado')
    return redirect(url_for('index'))

app.run(debug = True)