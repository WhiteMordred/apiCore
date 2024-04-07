from flask import current_app
from tools.datastore import Datastore
import uuid
from models.securityModel import SecurityModel
import json


def init():
    encryption_key = current_app.config['SECURITYKEY']
    datastore = Datastore(current_app.config['ORGANIZATION_DB'])
    organization = datastore.get_all_objects("init")

    if not organization:
        organization_config = {
            '_id': str(uuid.uuid4()),
            'organization_name': current_app.config['ORGANIZATION_NAME'],
            'address': current_app.config['ORGANIZATION_ADDRESS'],
            'city': current_app.config['ORGANIZATION_CITY'],
            'zipcode': current_app.config['ORGANIZATION_ZIPCODE'],
            'country': current_app.config['ORGANIZATION_COUNTRY'],
            'email': current_app.config['ORGANIZATION_EMAIL'],
            'phone': current_app.config['ORGANIZATION_PHONE'],
            'is_verified': True
        }

        model = SecurityModel(encryption_key, **organization_config)
        encrypted_data = model.to_dict()
        datastore.insert_object('init', encrypted_data)
        current_app.config['ORGANIZATION_ID'] = organization_config['_id']
        print('Organization is create successfully')
    else:
        print('Organization is allready created')
