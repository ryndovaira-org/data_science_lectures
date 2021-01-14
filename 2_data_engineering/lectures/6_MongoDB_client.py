from pymongo import MongoClient
import datetime

# https://api.mongodb.com/python/current/tutorial.html
try:
    # MongoClient('mongodb://localhost:27017/')
    client = MongoClient('localhost', 27017)
    print('client: ', client)

    # db = client['test-database']
    db = client['test-database']
    print('db: ', db)

    # collection = db['test_collection']
    collection = db.test_collection
    print('collection: ', collection)

    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}

    post_id = db.test_collection.insert_one(post).inserted_id
    print('post_id: ', post_id)

    print('db.list_collection_names(): ', db.list_collection_names())

    print('db.test_collection.find_one(): ', db.test_collection.find_one())

    print('db.test_collection.find_one({"author": "Mike"}): ', db.test_collection.find_one({"author": "Mike"}))
    print('db.test_collection.find_one({"author": "Eliot"}): ', db.test_collection.find_one({"author": "Eliot"}))

except Exception as err:
    print(err)



