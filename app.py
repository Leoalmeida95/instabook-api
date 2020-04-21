from flask import Flask, jsonify, redirect
from flask_restful import Api
from resources.hotelResources import Hoteis, Hotel
from resources.usuarioResources import Usuario, UsuarioRegistro, UsuarioLogin, UsuarioLogout, UsuarioConfirmacao
from resources.sitesResources import Sites, Site
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from blacklist import BLACKLIST
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = True
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone' #pode ser qualque string
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

SWAGGER_URL = '/api/docs'
API_URL= '/static/swagger-v3.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Swagger - Instabook"
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

@app.route('/')
@cross_origin()
def hello():
    return redirect("/api/docs", code=302)

#hotel
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:id>')
#usuario
api.add_resource(Usuario, '/usuario/<int:user_id>')
api.add_resource(UsuarioConfirmacao, '/usuario/confirmacao/<int:user_id>')
api.add_resource(UsuarioRegistro, '/usuario/')
api.add_resource(UsuarioLogin, '/usuario/login')
api.add_resource(UsuarioLogout, '/usuario/logout')
#site
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)