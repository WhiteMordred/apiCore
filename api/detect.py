from flask import request, jsonify, Blueprint, current_app
from tools.datastore import Datastore
from tools.mail_loader import registrationMailOrganization, registrationMailUser
from tools.wrapper_base64 import decode_base64_to_json
import bcrypt
import uuid
import os
from models.securityModel import SecurityModel
import base64
import json

detect_api = Blueprint('detect', __name__)

def generate_key():
    key = os.urandom(32)
    key_base64 = base64.urlsafe_b64encode(key).decode('utf-8')
    return jsonify({"key": key_base64}), 200

@detect_api.route('/detect_organization_mode', methods=['GET'])
def detect_organization_mode():
    if current_app.config['ORGANIZATION_MODE'] == 'standalone':
        return jsonify({"organization_mode": "standalone"}), 200
    else:
        return jsonify({"organization_mode": "multi"}), 200

@detect_api.route('/detect_organization_standalone', methods=['GET'])
def detect_organization_standalone():
    session_uuid = request.args.get('sessionUUID')
    datastore = Datastore(current_app.config['ORGANIZATION_DB'])
    detect_organization_data= {}
    organization = datastore.get_all_objects('init')
    print(organization)
    if not (organization):
        pass
    else:
        encrytion_key = current_app.config['SECURITYKEY']
        model = SecurityModel(encrytion_key)
        organization = organization[0]
        detect_organization_data["_id"]= str(uuid.uuid4())
        detect_organization_data['Organization _id'] = model.decrypt_string(organization['_id'])
        detect_organization_data['Session_id'] = session_uuid
        detect_organization_data['Url'] = current_app.config['FRONTEND_URL'] + "/register-user?session_id=" + detect_organization_data['Session_id']
        detect_organization_data['IsChecked'] = False
        encrypted_data = model.encrypt_dict(detect_organization_data)
        session_uuid_encrypted = model.encrypt_string(session_uuid)
        IfSessionUuid = datastore.get_object_by_field('nfa', 'Session_id', session_uuid_encrypted)
        if not IfSessionUuid:
            if not session_uuid_encrypted:
                pass
            else:
                datastore.insert_object('nfa', encrypted_data)
            return jsonify({"objet": detect_organization_data}), 201
        else:
            return jsonify({"objet": detect_organization_data}), 201
        

@detect_api.route('/detect_organization_multi', methods=['GET'])
def detect_organization_multi():
    session_uuid = request.args.get('sessionUUID')
    encryption_key = current_app.config['SECURITYKEY']
    data = request.get_json(force=True)
    datastore = Datastore(current_app.config['ORGANIZATION_DB'])
    model = SecurityModel(encryption_key, **data)
    detect_organization_data= {}
    organization = datastore.get_all_objects('init')
    if not (organization):
        pass
    else:
        organization = organization[0]
        detect_organization_data['Organization _id'] = organization['_id']
        detect_organization_data['Session_id'] = session_uuid
        detect_organization_data['Url'] = current_app.config['FRONTEND_URL'] + "/registration_device?session_id=" + detect_organization_data['Session_id']
        detect_organization_data['IsChecked'] = False
        return jsonify({"objet": detect_organization_data}), 201