import os
import connexion
import datetime
import logging
import time

from connexion import NoContent

PETS={}

def get_pets(limit, animal_type=None):
    return {"pets": [pet for pet in PETS.values() if not animal_type or pet['animal_type'] == animal_type][:limit]}

def get_pet(pet_id):
    pet=PETS.get(pet_id)
    return pet or ('Not Found', 404)

def post_pet(pet):
    pet_id=str(time.time())[-5:]
    pet['id']=pet_id
    logging.info('Creating pet %s ...', pet_id)
    pet['created']=datetime.datetime.utcnow()
    PETS[pet_id] = pet    
    return pet, 201


def put_pet(pet_id, pet):
    exists=pet_id in PETS
    print('exists:', exists)
    pet['id']=pet_id
    if exists:
        logging.info('Updating pet %s ...', pet_id)
        PETS[pet_id].update(pet)
    else:
        logging.info('FAILED Updating pet %s ...', pet_id)
        return NoContent, 404
    return pet, 200

def delete_pet(pet_id):
    if pet_id in PETS:
        logging.info('Deleting pet %s ...', pet_id)
        del PETS[pet_id]
        return NoContent, 204
    else:
        return NoContent, 404


logging.basicConfig(level=logging.INFO)
app=connexion.App(__name__, specification_dir='swagger/')
app.add_api('pets.yaml')
application=app.app

if __name__=='__main__':
    #app.run(port=8080) #,server='gevent'
    app.run(port=int(os.environ.get('PORT', 8080)))
