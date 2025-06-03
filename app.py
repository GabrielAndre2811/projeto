from flask import Flask
from routes.main_routes import main_bp
from routes.usuario_routes import usuario_bp
from routes.carrinho_routes import carrinho_bp

app = Flask(__name__)
app.secret_key = 'yahoo'

# Registrar os blueprints
app.register_blueprint(main_bp)
app.register_blueprint(usuario_bp, url_prefix='/usuario')
app.register_blueprint(carrinho_bp, url_prefix='/carrinho')

if __name__ == '__main__':
    app.run(debug=True)
