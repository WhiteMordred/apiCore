from flask import request, jsonify, Blueprint, current_app
from tools.datastore import Datastore
import bcrypt
import jwt
from datetime import timedelta, datetime

ACCESS_TOKEN_EXPIRE_MINUTES = 60

authentication_api = Blueprint('authentication', __name__)

@authentication_api.route('/authentication', methods=['GET'])
def authentication():
    datastore = Datastore('init')
    data = request.get_json()
    organization_id = data["organization_id"]
    username = data["username"]
    provided_password = data["password"]
    organization_details = datastore.get_object_by_field("organizations", "_id", organization_id)
    if organization_details:
        if organization_details.get('is_verified') is True:
            specific_database = Datastore(organization_details['organization_db'])
            print(specific_database)
            user = specific_database.get_object_by_field('users', 'username', username)
            if user and bcrypt.checkpw(provided_password.encode('utf-8'), user['password'].encode('utf-8')):
                return jsonify({"success": True, "access_token": create_access_token(identity=username)}), 200
            else:
                return jsonify({"success": False, "message": "Invalid credentials."}), 401
        else:
            return jsonify({"success": False, "message": "Organization not verified."}), 403
    else:
        return jsonify({"success": False, "message": f"Organization '{organization_id}' does not exist."}), 404

def create_access_token(user):
    dt = datetime.utcnow()
    expiry = dt + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {
      "sub": str(user["_id"]),
      "exp": expiry,
      "iat": dt
    }

    encoded_jwt = jwt.encode(claims, current_app.secret_key, algorithm="HS256")
    return encoded_jwt
