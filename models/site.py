from sql_alchemy import banco

class SiteModel(banco.Model):
    __tablename__='site'

    id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    def __init__(self, url:
        self.url = url


    def json(self):
        return{
            'id': self.id,
            'url': self.url,
            'hotis': [hotel.json() for hotel in self.hoteis]
        }

    #cls define que o método é um 'método de classe', portanto não acessa as propriedades self
    @classmethod
    def find(cls, url):
        site = cls.query.filter_by(url=url).first()
        return site if site else None

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        banco.session.delete(self)
        banco.session.commit()