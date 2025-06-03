from flask import Blueprint, render_template, request, session, redirect, url_for

carrinho_bp = Blueprint('carrinho', __name__)

@carrinho_bp.route('/adicionar', methods=['POST'])
def adicionar_carrinho():
    item = {
        'nome': request.form['nome'],
        'preco': float(request.form['preco']),
        'tipo': request.form['tipo']
    }
    if 'carrinho' not in session:
        session['carrinho'] = []
    session['carrinho'].append(item)
    session.modified = True
    return redirect(url_for('carrinho.ver_carrinho'))

@carrinho_bp.route('/')
def ver_carrinho():
    return render_template('carrinho.html', carrinho=session.get('carrinho', []))

@carrinho_bp.route('/remover_item/<int:item_index>')
def remover_item(item_index):
    if 'carrinho' in session and 0 <= item_index < len(session['carrinho']):
        session['carrinho'].pop(item_index)
        session.modified = True
    return redirect(url_for('carrinho.ver_carrinho'))

@carrinho_bp.route('/finalizar')
def finalizar_compra():
    if 'carrinho' in session:
        total = sum(item['preco'] for item in session['carrinho'])
        session.pop('carrinho', None)
        return render_template('finalizar_compra.html', total=total)
    else:
        return redirect(url_for('carrinho.ver_carrinho'))
