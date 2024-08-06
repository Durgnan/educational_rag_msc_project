import pymongo
from pymongo import MongoClient
from mongoengine import connect
import os

def connect_db():
    db = connect(host=os.getenv('MONGO_URI'))
    # client = MongoClient(os.getenv('MONGO_URI'))
    # db = client['ed_rag']
    return db


