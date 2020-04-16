from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis =[
        {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 600,
        'cidade': 'Rio de Janeiro'
        },
        {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 5,
        'diaria': 100,
        'cidade': 'São Paulo'
        },
        {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 2.6,
        'diaria': 310,
        'cidade': 'Acre'
        }
]

class Hoteis(Resource):

    def get(self):
        hoteis = HotelModel.find_all()

        return {'hoteis': [ hotel.json() for hotel in hoteis if hoteis is not None ]}

        return {'message': 'Hotel not found.'}, 404

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

    def delete(self, hotel_id):
        hotel_encontrado = HotelModel.find(hotel_id)
        if hotel_encontrado:
            try:
                hotel_encontrado.delete()
                return {'message': 'Hotel deleted.'}
            except:
                return {'message':'An internal error ocurred trying to delete "hotel".'}, 500

        return {'message': 'Hotel not found.'}, 404