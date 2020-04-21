from flask import Flask, jsonify
from flask_restful import Api
from resources.hotelResources import Hoteis, Hotel
from resources.usuarioResources import Usuario, UsuarioRegistro, UsuarioLogin, UsuarioLogout
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone' #pode ser qualque string
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

SWAGGER_URL = '/swagger'
API_URL= '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'messefe': 'You have been logged out'}), 401

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.before_first_request
def cria_banco():
    banco.create_all()

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(Usuario, '/usuario/<int:user_id>')
api.add_resource(UsuarioRegistro, '/usuario/')
api.add_resource(UsuarioLogin, '/usuario/login')
api.add_resource(UsuarioLogout, '/usuario/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)