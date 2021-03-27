from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json




app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://samy:samy@resto.1ssrd.mongodb.net/restaurants?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():

    Nom = request.json['Nom']
    Adresse = request.json['Adresse']
    Commune = request.json['Commune']
    Type = request.json['Type']
    Contact = request.json['Contact']
    Service = request.json['Service']
    Disponibilites = request.json['Disponibilites']
    image = request.json['image']

    if Nom and Adresse and Commune and Type and Contact and Service and Disponibilites :
        id = mongo.db.users.insert(
            {'Nom': Nom, 'Adresse': Adresse, 'Commune': Commune, 'Type':Type, 'Contact':Contact, 'Service':Service, 'Disponibilites': Disponibilites, 'image':image})
        response = {
            '_id': str(id),
            'Nom': Nom,
            'Adresse': Adresse, 
            'Commune': Commune, 
            'Type':Type, 
            'Contact':Contact, 
            'Service':Service, 
            'Disponibilites': Disponibilites,
            'image':image
        }

        return response
    else : 
            return not_found()

    return {'message':'received'}


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")



@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id) })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User ' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    
    Nom = request.json['Nom']
    Adresse = request.json['Adresse']
    Commune = request.json['Commune']
    Type = request.json['Type']
    Contact = request.json['Contact']
    Service = request.json['Service']
    Disponibilites = request.json['Disponibilites']
    image = request.json['image']

    if _id :

        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
             {'$set': {'Nom': Nom, 'Adresse': Adresse, 'Commune': Commune,'Type':Type, 'Contact': Contact,
              'Service': Service, 'Disponibilites':Disponibilites, 'image': image }})


        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()



@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return message


if __name__ =="__main__":
    app.run(debug=True) 