from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__='hotel'

    id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    site_id = banco.Column(banco.Integer, banco.ForeignKey('site.id'))

    def __init__(self, id, nome, estrelas, diaria, cidade, site_id):
        self.id = id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id

    def json(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id': self.site_id
        }

    #cls define que o método é um 'método de classe', portanto não acessa as propriedades self
    @classmethod
    def find(cls, id):
        hotel = cls.query.filter_by(id=id).first()
        return hotel if hotel else None

    @classmethod
    def find_all(cls):
        hoteis = cls.query.all()
        return hoteis 

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def update(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete(self):
        banco.session.delete(self)
        banco.session.commit()