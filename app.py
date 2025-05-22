from flask import Flask, render_template, request, redirect

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


if __name__ == '__main__':
    app.run(debug=True)
