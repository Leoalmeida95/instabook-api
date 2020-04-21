from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required
from resources.filtrosResources import normalize_path_params, consulta_padrao, consulta_cidade
import sqlite3



path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('offset', type=float)
path_params.add_argument('limit', type=float)


class Hoteis(Resource):

    def get(self):

        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        # hoteis = HotelModel.find_all()
        dados = path_params.parse_args()
        dados_buscados = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_buscados)
        tupla = tuple([parametros[chave] for chave in parametros])
   
        result = cursor.execute(consulta_padrao if not parametros.get('cidade') else consulta_cidade,
                 tupla)

        hoteis = []
        for linha in result:
            hoteis.append({
            'id': linha[0],
            'nome': linha[1],
            'estrelas': linha[2],
            'diaria': linha[3],
            'cidade': linha[4],
            'site_id': linha[5]
            })

        if hoteis:
            return {'hoteis': hoteis}, 200

        return {'message': 'No Hotels found.'}, 204

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria', type=float, required=True, help="The field 'diaria' cannot be left blank.")
    argumentos.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be left blank.")
    argumentos.add_argument('site_id', type=int, required=True, help="The field 'site_id' cannot be left blank.")

    def get(self, id):
        hotel = HotelModel.find(id)

        if hotel:
            return hotel.json(), 200

        return {'message': 'Hotel not found.'}, 204

    @jwt_required
    def post(seidlf, id):
        if HotelModel.find(id):
            return{"message":"Hotel id '{}' already exists.".format(id)}, 400

        dados = Hotel.argumentos.parse_args()
        novo_hotel = HotelModel(id, **dados) #implementando o **kwargs, distribuindo as propriedades de chave e valor pelo objeto

        if not SiteModel.find_by_id(novo_hotel.site_id):
            return{"message": "Site id '{}' not exists.".format(novo_hotel.site_id)}, 400

        try:
            novo_hotel.save()
        except Exception as e:
            return {"message":"An internal error ocurred trying to save 'hotel'."}, 500

        return novo_hotel.json(), 201

    @jwt_required
    def put(self, id):
        hotel_encontrado = HotelModel.find(id)
        dados = Hotel.argumentos.parse_args()
        try:
            if hotel_encontrado:
                hotel_encontrado.update(**dados)
                return hotel_encontrado.json(), 200

            novo_hotel = HotelModel(id, **dados)
            novo_hotel.save()
        except Exception as e:
            print (e)
            return {"message":"An internal error ocurred trying to update 'hotel'."}, 500

        return novo_hotel.json(), 201

    @jwt_required
    def delete(self, id):
        hotel_encontrado = HotelModel.find(id)
        if hotel_encontrado:
            try:
                hotel_encontrado.delete()
                return {'message': 'Hotel deleted.'}, 200
            except:
                return {'message':'An internal error ocurred trying to delete "hotel".'}, 500

        return {'message': 'Hotel not found.'}, 404