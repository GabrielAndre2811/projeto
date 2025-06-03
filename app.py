from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acesso', methods=['POST'])
def acesso():
    username = request.form['login']
    password = request.form['password']
    
    if username == 'gabriel@' and password == '123':
        return redirect('/servicos')
    else:
        print('Usuário não encontrado')
        return "Usuário ou senha incorretos", 401

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/add_cadastro', methods=['POST'])
def add_cadastro():
    email = request.form['email']
    login = request.form['login']
    senha = request.form['senha']
    nome = request.form['nome']
    datanascimento = request.form['data-nascimento']
    cpf = request.form['cpf']
    telefone = request.form['telefone']

    print(f'Cadastro realizado com sucesso: {email}, {login}, {nome}, {datanascimento}, {cpf}, {telefone}')
    return redirect('/servicos')
    














@app.route('/adicionar_carrinho', methods=['POST'])
def adicionar_carrinho():
    item = {
        'nome': request.form['nome'],
        'preco': float(request.form['preco']),
        'tipo': request.form['tipo']
    }
    if 'carrinho' not in session:
        session['carrinho'] = []
    session['carrinho'].append(item)
    session.modified = True  # necessário para atualizar a sessão corretamente
    return redirect('/carrinho')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html', carrinho=session.get('carrinho', []))

@app.route('/remover_item/<int:item_index>')
def remover_item(item_index):
    if 'carrinho' in session and 0 <= item_index < len(session['carrinho']):
        session['carrinho'].pop(item_index)
        session.modified = True
    return redirect('/carrinho')

@app.route('/finalizar_compra')
def finalizar_compra():
    if 'carrinho' in session:
        total = sum(item['preco'] for item in session['carrinho'])
        session.pop('carrinho', None)
        return render_template('finalizar_compra.html', total=total)
    else:
        return redirect('/carrinho')
    
@app.route('/logout')
def logout():
    session.pop('carrinho', None)
    return redirect('/')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')


if __name__ == '__main__':
    app.run(debug=True)
