from flask_restful import Resource, reqparse
from models.usuarioModel import UsuarioModel

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
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help='The field "login" cannot be left blank.')
        atributos.add_argument('senha', type=str, required=True, help='The field "senha" cannot be left blank.')
        dados = atributos.parse_args()

        if UsuarioModel.find_by_login(dados['login']):
            return {'message': 'The login "{}" already exists.'.format(dados['login'])}

        user = UsuarioModel(**dados)
        user.save()
        return {'message':'User created!'}, 201