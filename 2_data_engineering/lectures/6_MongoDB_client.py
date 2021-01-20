from pymongo import MongoClient
import datetime
import pprint

print(f"{'-'*50}\n")

# -----Подключение----------------------------------------------------------------

# Установление соединения с MongoClient
# MongoClient('mongodb://localhost:27017/')
client = MongoClient('localhost', 27017)
print(f"client: {client}\n")

# Получение базы данных
# db = client['test-database']
db = client['test-database']
print(f"db: {db}\n")

# Получение коллекции
# collection = db['test_collection']
collection = db.test_collection
print(f"collection: {collection}\n")
print(f"{'-'*50}\n")

# ------Добавление------------------------------------------------------------------------------------------------------
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

# добавить один документ и получить его id
post_id = db.test_collection.insert_one(post).inserted_id
print(f"db.test_collection.insert_one(post).inserted_id: {post_id}\n")

# DeprecationWarning: insert is deprecated. Use insert_one or insert_many instead
# post_id = db.test_collection.insert(post)
# print(f"insert(post).inserted_id: {post_id}\n")

# ------Обновление------------------------------------------------------------------------------------------------------

# ------Удаление--------------------------------------------------------------------------------------------------------

# ------Запросы---------------------------------------------------------------------------------------------------------

# получить имена коллекций из БД
print('db.list_collection_names(): ', db.list_collection_names())

# получить один любой документ из коллекции
print('db.test_collection.find_one(): ')
pprint.pprint(db.test_collection.find_one())
print()

print('db.test_collection.find_one({"author": "Mike"}: ', db.test_collection.find_one({"author": "Mike"}))
print('db.test_collection.find_one({"author": "Eliot"}): ', db.test_collection.find_one({"author": "Eliot"}))






