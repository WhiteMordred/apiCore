from pymongo import MongoClient
from tools.mongodb_loader import init_mongo_db, init_mongo_db_container
import uuid
from bson import Binary

class Datastore:
    def __init__(self,db_name):
        self.client = init_mongo_db()
        self.db = self.client[db_name]

    def get_all_objects(self, collection_name):
        collection = self.db[collection_name]
        return list(collection.find())

    def get_object(self, collection_name, object_id):
        collection = self.db[collection_name]
        return collection.find_one({"_id": object_id})

    def insert_object(self, collection_name, data):
        if '_id' not in data: 
            data['_id'] = str(uuid.uuid4())
        if '$binary' in data and 'hashed_password' in data:
            data['hashed_password'] = Binary(data['hashed_password']['$binary']['base64'], data['hashed_password']['$binary']['subType'])
        collection = self.db[collection_name]
        inserted_id = collection.insert_one(data).inserted_id
        return str(inserted_id)

    def update_object(self, collection_name, object_id, data):
        collection = self.db[collection_name]
        collection.update_one({"_id": object_id}, {"$set": data})

    def delete_object(self, collection_name, object_id):
        collection = self.db[collection_name]
        collection.delete_one({"_id": object_id})

    def delete_all(self, collection_name):
        collection = self.db[collection_name]
        collection.delete_many({})

    def get_object_by_field(self, collection_name, field_name, field_value):
        collection = self.db[collection_name]
        return collection.find_one({field_name: field_value})

    def get_object_by_field_and_origin(self, collection_name, field_name, field_value, origin_field_name, origin_value):
        collection = self.db[collection_name]
        return collection.find_one({field_name: field_value, origin_field_name: origin_value})

    def get_all_objects_by_origin(self, collection_name, origin_field_name, origin_value):
        collection = self.db[collection_name]
        return list(collection.find({origin_field_name: origin_value}))

    def check_object_exists(self, collection_name, field_name, field_value):
        collection = self.db[collection_name]
        return collection.find_one({field_name: field_value}) is not None

    def check_object_exists_with_args(self, collection_name, **kwargs):
        collection = self.db[collection_name]
        return collection.find_one(kwargs) is not None

    def get_object_by_fields(self, collection_name, **kwargs):
        collection = self.db[collection_name]
        return collection.find_one(kwargs)

    def get_object_by_fields_list(self, collection_name, **kwargs):
        collection = self.db[collection_name]
        return list(collection.find(kwargs))

    def search_documents(self, collection_name, query):
        if '.' in collection_name:
            sub_objects = collection_name.split('.')
            collection_name = sub_objects[0]
            for sub_object in sub_objects[1:]:
                query = {f"{sub_object}.{k}": v for k, v in query.items()}
        collection = self.db[collection_name]
        cursor = collection.find(query)
        documents = [doc for doc in cursor]
        return documents

    def close(self):
        if self.client:
            self.client.close()


class DatastoreContainer:
    def __init__(self,container_name, db_name):
        self.client = init_mongo_db_container(container_name)
        self.db = self.client[db_name]

    def get_all_objects(self, collection_name):
        collection = self.db[collection_name]
        return list(collection.find())

    def get_object(self, collection_name, object_id):
        collection = self.db[collection_name]
        return collection.find_one({"_id": object_id})

    def insert_object(self, collection_name, data):
        if '_id' not in data: 
            data['_id'] = str(uuid.uuid4())
        if '$binary' in data and 'hashed_password' in data:
            data['hashed_password'] = Binary(data['hashed_password']['$binary']['base64'], data['hashed_password']['$binary']['subType'])
        collection = self.db[collection_name]
        inserted_id = collection.insert_one(data).inserted_id
        return str(inserted_id)

    def update_object(self, collection_name, object_id, data):
        collection = self.db[collection_name]
        collection.update_one({"_id": object_id}, {"$set": data})

    def delete_object(self, collection_name, object_id):
        collection = self.db[collection_name]
        collection.delete_one({"_id": object_id})

    def delete_all(self, collection_name):
        collection = self.db[collection_name]
        collection.delete_many({})

    def get_object_by_field(self, collection_name, field_name, field_value):
        collection = self.db[collection_name]
        return collection.find_one({field_name: field_value})

    def get_object_by_field_and_origin(self, collection_name, field_name, field_value, origin_field_name, origin_value):
        collection = self.db[collection_name]
        return collection.find_one({field_name: field_value, origin_field_name: origin_value})

    def get_all_objects_by_origin(self, collection_name, origin_field_name, origin_value):
        collection = self.db[collection_name]
        return list(collection.find({origin_field_name: origin_value}))

    def check_object_exists(self, collection_name, field_name, field_value):
        collection = self.db[collection_name]
        return collection.find_one({field_name: field_value}) is not None

    def check_object_exists_with_args(self, collection_name, **kwargs):
        collection = self.db[collection_name]
        return collection.find_one(kwargs) is not None

    def get_object_by_fields(self, collection_name, **kwargs):
        collection = self.db[collection_name]
        return collection.find_one(kwargs)

    def get_object_by_fields_list(self, collection_name, **kwargs):
        collection = self.db[collection_name]
        return list(collection.find(kwargs))

    def search_documents(self, collection_name, query):
        if '.' in collection_name:
            sub_objects = collection_name.split('.')
            collection_name = sub_objects[0]
            for sub_object in sub_objects[1:]:
                query = {f"{sub_object}.{k}": v for k, v in query.items()}
        collection = self.db[collection_name]
        cursor = collection.find(query)
        documents = [doc for doc in cursor]
        return documents

    def close(self):
        if self.client:
            self.client.close()