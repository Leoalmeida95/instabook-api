from flask_restful import Resource, reqparse
from models.usuarioModel import UsuarioModel

class Usuario(Resource):
    #usuario
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