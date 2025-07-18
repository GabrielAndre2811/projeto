from flask import Blueprint, render_template, request, redirect, session, url_for
import secrets
import logging


logging.basicConfig(level=logging.INFO)

usuario_bp = Blueprint('usuario', __name__)

USERS = { 
    "gabriel@": "123"
}

@usuario_bp.route('/login')
def login():
    return render_template('login.html')

@usuario_bp.route('/servicos')
def servicos():
    getuser = session.get('usuario')
    return render_template('servicos.html', nomeuser="Gabriel")

@usuario_bp.route('/acesso', methods=['POST'])
def acesso():
    username = request.form['login']
    password = request.form['password']




    if username in USERS and USERS[username] == password:
        session['usuario'] = username
        # Em um cenário real, você geraria um token de autenticação válido
        # Simulando um token de autenticação
        token = "1234"
       # token = secrets.token_hex(16)
        session['token'] = token
        return redirect(url_for('usuario.servicos'))
    else:
        session.pop('usuario', None)
        return "Usuário ou senha incorretos", 401

@usuario_bp.route('/cadastro')
def cadastro():

    return render_template('cadastro.html')

@usuario_bp.route('/add_cadastro', methods=['POST'])
def add_cadastro():
    email = request.form['email']
    login = request.form['login']
    senha = request.form['senha']
    nome = request.form['nome']
    datanascimento = request.form['data-nascimento']
    cpf = request.form['cpf']
    telefone = request.form['telefone']


    session['usuario'] = {
        'email': email,
        'login': login,
        'nome': nome,
        'datanascimento': datanascimento,
        'cpf': cpf,
        'telefone': telefone
    }

    if email in USERS:
        logging.warning(f'Usuário já cadastrado: {login}')
        return "Usuário já cadastrado", 400

    USERS[email] = senha
    logging.info(f'Cadastro realizado com sucesso: {email}, {login}, {nome}, {datanascimento}, {cpf}, {telefone}')
    return redirect(url_for('usuario.servicos'))


@usuario_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Isso já apaga tudo: usuario, token, etc
    return redirect(url_for('usuario.login'))



@usuario_bp.before_request
def check_auth():
    rotas_livres = [
        'usuario.login',
        'usuario.logout',
        'usuario.acesso',
        'usuario.cadastro',
        'usuario.add_cadastro'
    ]

    print("Endpoint acessado:", request.endpoint)  # Ajuda no debug

    if request.endpoint in rotas_livres:
        return

    token = session.get('token')
    if token:
        return  # Está autenticado

    return redirect(url_for('usuario.login'))
