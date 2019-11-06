from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = 'caiao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogo.db'
# @app.route("/")
# def hello():
#     return "HelloWorld!"

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, username, nome, senha, email):
        self.username = username
        self.nome = nome
        self.email = email
        self.senha = senha

usuario1 = Usuario('luan', 'Luan Marques', '1234', 'luan')
usuario2 = Usuario('2', 'Caio', '3540', 'caiao')
usuario3 = Usuario('3', 'Carol', '9876', 'carol')

usuarios = { usuario1.username: usuario1,
             usuario2.username: usuario2,
             usuario3.username: usuario3}

jogo1 = Jogo('Super Mario', 'Acao', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
lista = [jogo1, jogo2]       


@app.route('/')
def index():
    return render_template('lista.html', titulo = 'Jogos', jogos = lista)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('cadastro')))
    return render_template('cadastro.html', titulo = 'Cadastre o seu novo Jogo')

@app.route('/criar_jogo', methods = ['POST',])
def criar_jogo():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
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


    # if  'mestra' == request.form['senha']:
    #     session ['usuario_logado'] = request.form['usuario']
    #     flash(request.form['usuario'] + 'logado')
    #     proxima_pagina = request.form['proxima']
    #     return redirect(proxima_pagina)
    # else:
    #     flash('Não logado, tente de novo!')
    #     return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('None user logado')
    return redirect(url_for('index'))

app.run(debug = True)