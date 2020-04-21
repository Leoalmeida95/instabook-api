from flask_restful import Resource, reqparse
from models.site import SiteModel
from flask_jwt_extended import jwt_required

class Sites(Resource):
    def get(self):
        sites = SiteModel.find_all()

        if sites:
            return {'sites': [site.json() for site in sites]}, 200

        return {'message': 'No Sites found.'}, 404

class Site(Resource):
    def get(self, url):
        site = SiteModel.find(url)

        if site:
            return site.json(), 200
        
        return {'message': 'Site not found.'}, 404

    @jwt_required
    def post(self, url):

        if SiteModel.find(url):
            return {'message': 'The Site already exists.'}, 422
        
        novo_site = SiteModel(url)

        try:
            novo_site.save()
        except Exception as e:
            return {"message":"An internal error ocurred trying to save 'site'."}, 500

        return novo_site.json(), 201

    @jwt_required
    def delete(self, url):
        site_encontrado = SiteModel.find(url)
        if site_encontrado:
            try:
                site_encontrado.delete()
                return {'message': 'Site deleted.'}, 200
            except Exception as e:
                return {"message":"An internal error ocurred trying to delete 'site'."}, 500

        return {'message': 'Site not found.'}, 404
        