from sql_alchemy import banco
from flask import request, url_for
import requests
#credencias obtidas na conta wofsystem@gmail.com na mailgun
from credenciais_mailgun import MAIL_GUN_API_KEY, MAILGUN_DOMAIN

FORM_TITLE = 'NO-REPLAY'
FROM_EMAIL = 'no-reply@instabook.com'

class UsuarioModel(banco.Model):
    __tablename__='usuario'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    ativado = banco.Column(banco.Boolean)
    email = banco.Column(banco.String(40), nullable=False, unique=True)

    def __init__(self, login, senha, ativado, email):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = False

    def send_confirmacao_email(self):
        link = request.url_root[:-1] + url_for('usuarioconfirmacao', user_id=self.user_id)
        return requests.post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth=('api', MAIL_GUN_API_KEY),
                    data={'from': '{} <{}>'.format(FORM_TITLE, FROM_EMAIL),
                          'to': self.email,
                          'subject': 'Confirmação de Cadastro',
                          'text': 'Confirme seu Cadastro clicando no link a seguir: {}'.format(link),
                          'html': '<html><p>\
                            Confirme seu cadastro clicando no link a seguir: <a href="{}">CONFIRMAR EMAL</a>\
                            </p></html>'.format(link)
                          }
                    )



    def json(self):
        return{
            'user_id': self.user_id,
            'login': self.login,
            'ativado': self.ativado,
            'email': self.email
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

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        return user if user else None

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        banco.session.delete(self)
        banco.session.commit()