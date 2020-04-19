from flask_restful import Resource, reqparse
from models.usuarioModel import UsuarioModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The field "login" cannot be left blank.')
atributos.add_argument('senha', type=str, required=True, help='The field "senha" cannot be left blank.')

class Usuario(Resource):
    #/usuario/{user_id}
    def get(self, user_id):
        user = UsuarioModel.find(user_id)

        if user:
            return user.json()

        return {'message': 'User not found.'}, 404

    def delete(self, user_id):
        user = UsuarioModel.find(user_id)
        if user:
            try:
                user.delete()
                return {'message': 'User deleted.'}
            except:
                return {'message':'An internal error ocurred trying to delete "User".'}, 500

        return {'message': 'User not found.'}, 404

class UsuarioRegistro(Resource):
    #/cadastro
    def post(self):
        dados = atributos.parse_args()

        if UsuarioModel.find_by_login(dados['login']):
            return {'message': 'The login "{}" already exists.'.format(dados['login'])}

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
            token_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_acesso}, 200
        
        return {'message': 'User not find.'}, 401