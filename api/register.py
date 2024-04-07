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


ACCESS_TOKEN_EXPIRE_MINUTES = 60

register_api = Blueprint('register', __name__)

def generate_key():
    key = os.urandom(32)
    key_base64 = base64.urlsafe_b64encode(key).decode('utf-8')
    return jsonify({"key": key_base64}), 200


@register_api.route('/register_organization', methods=['POST'])
def register_organization():
    encryption_key = current_app.config['SECURITYKEY']
    datastore = Datastore(current_app.config['ORGANIZATION_DB'])
    try:
        data = request.get_json(force=True)
        if  'organization_name' not in data:
            return jsonify({"error": "manques des entrées users"}), 400
        data['organization_db'] = str(uuid.uuid4())
        data['_id'] = str(uuid.uuid4())
        data_encrypted = SecurityModel(encryption_key, **data)
        encrypted_user_data = data_encrypted.to_dict()
        datastore.insert_object("organizations", encrypted_user_data)
        key32 = os.urandom(32)
        key_base64 = base64.urlsafe_b64encode(key32).decode('utf-8')
        keydata={}
        keydata['organization_id'] = data['_id']
        keydata['organization_name'] = data['organization_name']
        keydata['_id']=str(uuid.uuid4())
        keydata['key'] = key_base64
        keyModel = SecurityModel(encryption_key, **keydata)
        encrypted_key_data = keyModel.to_dict()
        datastore.insert_object("keys", encrypted_key_data)
        verification_url = f"{current_app.config['FRONTEND_URL']}/verify_organization?id={data['_id']}&organization={data['organization_db']}"
        registration = {}
        registration['organization_id'] = data['_id']
        registration['organization_name'] = data['organization_name']
        registration['email'] = data['email']
        registration['verification_url'] = verification_url
        registration['frontend_url'] = current_app.config['FRONTEND_URL']
        registrationMailOrganization(registration=registration)
        return jsonify({"message": "Organization created successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Erreur interne serveur: {str(e)}"}), 500

@register_api.route('/register_user', methods=['POST'])
def register_user():
    try:
        data = request.get_json(force=True)
        cert = decode_base64_to_json(data['cert'])
        base_encryption_key = current_app.config['SECURITYKEY']
        base_model = SecurityModel(base_encryption_key)
        encryption_key = base_model.decrypt_string(cert[1])
        db = base_model.decrypt_string(cert[0])
        datastore = Datastore(db)
        userdata = data.copy()
        provided_password = userdata.pop('password')
        hashed_password = bcrypt.hashpw(provided_password.encode('utf-8'), bcrypt.gensalt())
        userdata['_id'] = str(uuid.uuid4())
        userdata['password'] = hashed_password.decode('utf-8')
        userdata['role']="admin"
        userdata['photo'] = data['photoDataUrl']
        userdata['birthday'] = data['birthday_day'] + "/" + data['birthday_month'] + "/" + data['birthday_year']
        recovery_model = SecurityModel(encryption_key)
        recovery_words = data['recovery'].split()
        encrypted_recovery_words = [recovery_model.encrypt_string(str(word.strip())) for word in recovery_words]
        keys_to_delete = ['cert', 'confirmPassword', 'recovery','photoDataUrl', 'birthday_day', 'birthday_month', 'birthday_year']
        for key in keys_to_delete:
            if key in userdata:
                del userdata[key]
            else:
                print(f"Key not found: {key}")
        model = SecurityModel(encryption_key, **userdata)
        encrypted_user_data = model.to_dict()
        encrypted_user_data['recovery'] = encrypted_recovery_words
        datastore.insert_object("users", encrypted_user_data)
        verification_url = f"{current_app.config['FRONTEND_URL']}/verify_user?id={userdata['_id']}"
        registration = {}
        registration['username'] = data['username']
        registration['verification_url'] = verification_url
        registration['email']=data['email']
        registrationMailUser(registration=registration)
        return jsonify({"message": "user succesfully created"}), 201
    except Exception as e:
        return jsonify({"error": f"Erreur interne serveur: {str(e)}"}), 500

