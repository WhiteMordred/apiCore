from flask import request, jsonify, Blueprint, current_app
from tools.datastore import Datastore
from tools.wrapper_base64 import encode_json_to_base64 
from models.securityModel import SecurityModel
from tools.passphrase_loader import recovery_passphrase

ACCESS_TOKEN_EXPIRE_MINUTES = 60

validate_api = Blueprint('validate', __name__)

@validate_api.route('/validate', methods=['GET'])
def validate():
    try:
        id = request.args.get('id')
        encryption_key = current_app.config['SECURITYKEY']
        model = SecurityModel(encryption_key)
        encrypted_id = model.encrypt_string(id)
        if not id:
            return jsonify({"error": "L'ID est requis"}), 400
        datastore = Datastore('init')
        organization = datastore.get_object('organizations',encrypted_id)
        if organization:
            organization['is_verified'] = True
            datastore.update_object('organizations', encrypted_id, organization)
            keystore = Datastore('keystore')
            organisation = keystore.get_object_by_field('keys','organization_id',encrypted_id)
            data=[]
            data.append(organisation['organization_id'])
            data.append(organisation['key'])
            encoded_json = encode_json_to_base64(data)
            recovery = recovery_passphrase()
            return jsonify({"message": "Compte vérifié","cert":encoded_json,"recovery":recovery}), 200
        return jsonify({"error": "Compte introuvable"}), 404
    except Exception as e:
        return jsonify({"error": f"Erreur interne serveur: {str(e)}"}), 500