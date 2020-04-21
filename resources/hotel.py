from flask_restful import Resource, reqparse
from models.hotelModel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(cidade=None,
                         estrelas_min=0,
                         estrelas_max=5,
                         diaria_min=0,
                         diaria_max=10000,
                         limit = 50,
                         offset = 0, **dados):
    result = {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diarias_min': diaria_min,
            'diarias_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }

    if not cidade: 
    #caso não haja cidade, é removida sem alterar a ordem dos demais parametros
        copy = dict(result)
        del copy['cidade']
        result = copy

    return result

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

        if not parametros.get('cidade'):
            consulta = "SELECT * FROM \
                                Hoteis \
                        WHERE (estrelas >= ? and estrelas <= ?)\
                              and (diaria >= ? and diaria <= ?)\
                        LIMIT ? \
                        OFFSET ? "
        else:
            consulta = "SELECT * FROM \
                                Hoteis \
                        WHERE (estrelas >= ? and estrelas <= ?)\
                              and (diaria >= ? and diaria <= ?)\
                              and cidade = ? \
                        LIMIT ? \
                        OFFSET ? "
                        
        result = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in result:
            hoteis.append({
            'hotel_id': linha[0],
            'nome': linha[1],
            'estrelas': linha[2],
            'diaria': linha[3],
            'cidade': linha[4]
            })

        if hoteis:
            return {'hoteis': hoteis}

        return {'message': 'No Hotels found.'}, 404

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria', type=float, required=True, help="The field 'diaria' cannot be left blank.")
    argumentos.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be left blank.")

    def get(self, hotel_id):
        hotel = HotelModel.find(hotel_id)

        if hotel:
            return hotel.json()

        return {'message': 'Hotel not found.'}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find(hotel_id):
            return{"message":"Hotel id '{}' already exists.".format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados) #implementando o **kwargs, distribuindo as propriedades de chave e valor pelo objeto
        try:
            novo_hotel.save()
        except:
            return {'message':'An internal error ocurred trying to update hotel.'}, 500

        return novo_hotel.json(), 200

    @jwt_required
    def put(self, hotel_id):
        hotel_encontrado = HotelModel.find(hotel_id)
        dados = Hotel.argumentos.parse_args()
        try:
            if hotel_encontrado:
                hotel_encontrado.update(**dados)
                hotel_encontrado.save()
                return hotel_encontrado.json(), 200

            novo_hotel = HotelModel(hotel_id, **dados)
            novo_hotel.save()
        except:
            return {'message':'An internal error ocurred trying to save "hotel".'}, 500

        return novo_hotel.json(), 201

    @jwt_required
    def delete(self, hotel_id):
        hotel_encontrado = HotelModel.find(hotel_id)
        if hotel_encontrado:
            try:
                hotel_encontrado.delete()
                return {'message': 'Hotel deleted.'}, 200
            except:
                return {'message':'An internal error ocurred trying to delete "hotel".'}, 500

        return {'message': 'Hotel not found.'}, 404