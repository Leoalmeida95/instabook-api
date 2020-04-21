from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The field "login" cannot be left blank.')
atributos.add_argument('senha', type=str, required=True, help='The field "senha" cannot be left blank.')
atributos.add_argument('ativado', type=bool, required=False)

class Usuario(Resource):
    #/usuario/{user_id}
    def get(self, user_id):
        user = UsuarioModel.find(user_id)

        if user:
            return user.json(), 200

        return {'message': 'User not found.'}, 404

    @jwt_required
    def delete(self, user_id):
        user = UsuarioModel.find(user_id)
        if user:
            try:
                user.delete()
                return {'message': 'User deleted.'}, 200
            except:
                return {'message':'An internal error ocurred trying to delete "User".'}, 500

        return {'message': 'User not found.'}, 404

class UsuarioRegistro(Resource):
    #/cadastro
    def post(self):
        dados = atributos.parse_args()

        if UsuarioModel.find_by_login(dados['login']):
            return {'message': 'The login "{}" already exists.'.format(dados['login'])}, 422

        user = UsuarioModel(**dados)
        user.save()

        return {'message':'User created!'}, 201

class UsuarioLogin(Resource):
    #login
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UsuarioModel.find_by_login(dados['login'])
        if user and safe_str_cmp(user.senha, dados['senha']):

            if user.ativado:
                token_acesso = create_access_token(identity=user.user_id)
                return {'access_token': token_acesso}, 200
            else:
                return {'message': 'User not confirmed.'}, 400
        
        return {'message': 'User not find.'}, 404

class UsuarioLogout(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        jwt_id = get_raw_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200

class UsuarioConfirmacao(Resource):

    @classmethod
    def get(cls, user_id):
        user = UsuarioModel.find(user_id)
        if user:
            try:
                user.ativado = True
                user.save()
                return {'message': 'User cofirmed!'}, 200
            except:
                return {"message":"An internal error ocurred trying to confirme email from 'User'."}, 500

        return {'message': 'User not found.'}, 404