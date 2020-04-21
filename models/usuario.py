from sql_alchemy import banco

class UsuarioModel(banco.Model):
    __tablename__='usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    # ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
        # self.ativado = ativado

    def json(self):
        return{
            'user_id': self.user_id,
            'login': self.login
            # 'ativado': self.ativado
        }

    #cls define que o método é um 'método de classe', portanto não acessa as propriedades self
    @classmethod
    def find(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        return user if user else None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        return user if user else None

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        banco.session.delete(self)
        banco.session.commit()