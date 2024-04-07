import os
from pymongo import MongoClient
from flask import current_app 

def init_mongo_db():
    uri = "mongodb://" + current_app.config['MONGO_INITDB_ROOT_USERNAME'] + ":" + current_app.config['MONGO_INITDB_ROOT_PASSWORD'] + "@" + current_app.config['MONGO_DB_HOST'] + ":" + current_app.config['MONGO_DB_PORT'] + "/"
    client = MongoClient(uri)
    return client

def init_mongo_db_container(container):
    uri=container
    client = MongoClient()
    return client
