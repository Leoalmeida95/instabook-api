from flask_restful import Resource, reqparse

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
        return {'hoteis': hoteis}

class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel

        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('nome')
        argumentos.add_argument('estrelas')
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')

        dados = argumentos.parse_args()

        novo_hotel = {
        'hotel_id': hotel_id,
        'nome': dados['nome'],
        'estrelas': dados['estrelas'],
        'diaria': dados['diaria'],
        'cidade': dados['cidade']
        }

        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):
        pass

    def delete(self, hotel_id):
        pass