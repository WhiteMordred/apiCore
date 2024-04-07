from flask import request, jsonify, Blueprint, current_app,render_template
from tools.datastore import Datastore, DatastoreContainer
import bcrypt
from tools.protected_routes import protected_route
from models.securityModel import SecurityModel

ACCESS_TOKEN_EXPIRE_MINUTES = 60

default_api = Blueprint('api', __name__)


@default_api.route('/<db>/<collection>/<action>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @protected_route(algorithms="HS256")
def handle_request(db, collection, action):
    """Handle CRUD operations."""  
    datastore = Datastore(db)
    # container_datastore = DatastoreContainer(container,db)

    if request.method == 'POST' and action == 'create':
        if collection == 'users':
            provided_password = request.get_json().get('password')
            if not provided_password:
                return jsonify({"error": "Missing 'password' property"}), 400

            hashed_password = bcrypt.hashpw(provided_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            del request.json['password']
            data = {'password': hashed_password, **request.json}

            inserted_id = datastore.insert_object(collection, data)
            return jsonify({"inserted_id": inserted_id}), 201
        else:
            data = request.get_json()

        inserted_id = datastore.insert_object(collection, data)
        return jsonify({"inserted_id": inserted_id}), 201

    elif request.method == 'GET' and action == 'read':
        document_id = request.args.get('id')
        document = datastore.get_object(collection, document_id)
        if document:
            return jsonify(document), 200
        else:
            return jsonify({"error": "Document not found"}), 404

    elif request.method == 'GET' and action == 'all':
        document = datastore.get_all_objects(collection)
        if document:
            return jsonify(list(document)), 200
        else:
            return jsonify({"error": "Document not found"}), 404

    elif request.method == 'PUT' and action == 'update':
        document_id = request.args.get('id')
        data = request.get_json()
        datastore.update_object(collection, document_id, data)
        return jsonify({"message": "Document updated"}), 200

    elif request.method == 'DELETE' and action == 'delete':
        document_id = request.args.get('id')
        datastore.delete_object(collection, document_id)
        return jsonify({"message": "Document deleted"}), 200

    elif request.method == 'PUT' and action == 'update_multiple':
        criteria = request.get_json()
        data = request.get_json()
        datastore.update_objects(collection, criteria, data)
        return jsonify({"message": "Documents updated"}), 200

    elif request.method == 'DELETE' and action == 'delete_multiple':
        criteria = request.get_json()
        count = datastore.delete_objects(collection, criteria)
        return jsonify({"message": f"{count} Documents deleted"}), 200

    elif request.method == 'GET' and action == 'get_object_by_field':
        field_name = request.args.get('field_name')
        field_value = request.args.get('field_value')
        document = datastore.get_object_by_field(collection, field_name, field_value)
        if document:
            return jsonify(document), 200
        else:
            return jsonify({"error": "Document not found"}), 404

    elif request.method == 'GET' and action == 'get_object_by_field_and_origin':
        field_name = request.args.get('field_name')
        field_value = request.args.get('field_value')
        origin_field_name = request.args.get('origin_field_name')
        origin_value = request.args.get('origin_value')
        document = datastore.get_object_by_field_and_origin(collection, field_name, field_value, origin_field_name, origin_value)
        if document:
            return jsonify(document), 200
        else:
            return jsonify({"error": "Document not found"}), 404

    elif request.method == 'GET' and action == 'get_all_objects_by_origin':
        origin_field_name = request.args.get('origin_field_name')
        origin_value = request.args.get('origin_value')
        document_list = datastore.get_all_objects_by_origin(collection, origin_field_name, origin_value)
        if len(document_list) > 0:
            return jsonify(document_list), 200
        else:
            return jsonify({"error": "No documents found"}), 404

    elif request.method == 'GET' and action == 'check_object_exists':
        field_name = request.args.get('field_name')
        field_value = request.args.get('field_value')
        exists = datastore.check_object_exists(collection, field_name, field_value)
        if exists:
            return jsonify({"exist": True}), 200
        else:
            return jsonify({"exist": False}), 200

    elif request.method == 'GET' and action == 'check_object_exists_with_args':
        kwargs = request.args.to_dict()
        exists = datastore.check_object_exists_with_args(collection, **kwargs)
        if exists:
            return jsonify({"exist": True}), 200
        else:
            return jsonify({"exist": False}), 200

    elif request.method == 'GET' and action == 'get_object_by_fields':
        kwargs = request.args.to_dict()
        document = datastore.get_object_by_fields(collection, **kwargs)
        if document:
            return jsonify(document), 200
        else:
            return jsonify({"error": "Document not found"}), 404

    elif request.method == 'GET' and action == 'get_object_by_fields_list':
        kwargs = request.args.to_dict()
        document_list = datastore.get_object_by_fields_list(collection, **kwargs)
        if len(document_list) > 0:
            return jsonify(document_list), 200
        else:
            return jsonify({"error": "No documents found"}), 404

    elif request.method == 'GET' and action == 'search_documents':
        query = request.args.to_dict()
        if '.' in collection:
            sub_objects = collection.split('.')
            collection = sub_objects[0]
            for sub_object in sub_objects[1:]:
                query = {f"{sub_object}.{k}": v for k, v in query.items()}
        cursor = collection.find(query)
        documents = [doc for doc in cursor]
        return jsonify(documents), 200

    else:
        return jsonify({"error": "Action not supported"}), 400


