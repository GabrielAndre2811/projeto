from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import secrets
import logging
import os
from werkzeug.utils import secure_filename


logging.basicConfig(level=logging.INFO)

usuario_bp = Blueprint('usuario', __name__)

USERS = { 
    "gabriel@": "123"
}

@usuario_bp.route('/login')
def login():
    return render_template('login.html')



# Configurações (defina na inicialização da sua app Flask)
UPLOAD_FOLDER = 'static/uploads'  # Pasta para salvar fotos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Função para checar extensões válidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@usuario_bp.route('/atualizar_dados', methods=['POST'])
def atualizar_dados():
    # Verifica se usuário está logado
    usuario = session.get('usuario')
    if not usuario:
        flash("Você precisa estar logado para atualizar seus dados.", "error")
        return redirect(url_for('usuario.login'))
    
    # Coleta dados do formulário
    nome = request.form.get('nome')
    email = request.form.get('email')
    datanascimento = request.form.get('datanascimento')
    cpf = request.form.get('cpf')
    telefone = request.form.get('telefone')
    senha = request.form.get('senha')

    # Verifica e salva a foto enviada (se houver)
    foto = request.files.get('foto')
    if foto and allowed_file(foto.filename):
        filename = secure_filename(foto.filename)
        
        # Certifique-se que a pasta existe
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        foto.save(filepath)

        # Salva o caminho da foto para usar no template
        usuario['foto_url'] = url_for('static', filename=f'uploads/{filename}')
    
    # Atualiza os dados do usuário na sessão (ou banco, se houver)
    usuario.update({
        'nome': nome,
        'email': email,
        'datanascimento': datanascimento,
        'cpf': cpf,
        'telefone': telefone
    })

    # Atualiza senha se foi preenchida
    if senha:
        USERS[email] = senha  # Atualize seu armazenamento conforme necessário
    
    # Atualiza sessão
    session['usuario'] = usuario

    flash("Dados atualizados com sucesso!", "success")
    return redirect(url_for('usuario.meus_dados'))

@usuario_bp.route('/meus_dados')
def meus_dados():
    usuario = session.get('usuario')
    return render_template('meus_dados.html')



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
        
        token = secrets.token_hex(16)
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


@usuario_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Issojá apaga tudo: usuario, token, etc
    return redirect(url_for('usuario.login'))


@usuario_bp.before_request
def check_auth():

    token = session.get('token')
    # Lista de rotas livres que não requerem autenticação
    
    rotas_livres = [
        'sobre',
        'contato', 
        'index',
        'usuario.login', 
        'usuario.logout',
        'usuario.acesso', 
        'usuario.cadastro', 
        'usuario.add_cadastro',
        'usuario.logout'
    ]

    #verifica as rotas livre e nao busca token de autenticação
    if request.endpoint in rotas_livres:
        return
    
    # Verifica se o token de autenticação está presente na sessão
    if not token:
        return redirect(url_for('usuario.login'))
    # Aqui você pode adicionar lógica para validar o token, se necessário
    # Por exemplo, verificar se o token é válido e não expirou      