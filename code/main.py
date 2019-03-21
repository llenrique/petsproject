from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
# JWT Json Web Token

from security import authenticate, identity
import os


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
api = Api(app)


jwt = JWT(app, authenticate, identity)

pets = []


class Owner(Resource):
    @jwt_required()
    def get(self, name):
        pet = next(filter(lambda x: x['name'] == name, pets), None)
        return ({'pet': pet}, 200 if pet is not None else 404)

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, pets), None):
            return {'message': 'name already taken'}, 400

        data = request.get_json(silent=True)
        pet = {
            'id': data['id'],
            'name': name,
            'race': data['race'],
            'age': data['age'],
            'personality': data['personality']
        }
        pets.append(pet)
        return pet, 201

    @jwt_required()
    def delete(self, name):
        global pets
        pets = list(filter(lambda x: x['name'] != name, pets))
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = request.get_json()
        pet = next(filter(lambda x: x['name'] == name, pets), None)
        if pet is None:
            pet = {
                'id': data['id'],
                'name': name,
                'race': data['race'],
                'age': data['age'],
                'personality': data['personality']
            }
            pets.append(pet)
        else:
            pet.update(data)
        return pet

class OwnerList(Resource):
    @jwt_required()
    def get(self):
        return ({'pets': pets})


api.add_resource(Owner, '/pet/<string:name>')
api.add_resource(OwnerList, '/pets')


if __name__ == '__main__':
    app.run(debug=True)
