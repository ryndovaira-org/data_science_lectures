# -----Импорт пакетов-------------------------------------------------------------

from bson import ObjectId
from pymongo import MongoClient
import datetime
import pprint

num_sep = 150
print(f"{'*' * num_sep}\n")

# -----Подключение----------------------------------------------------------------

# установить соединение с MongoClient
# MongoClient('mongodb://localhost:27017/')
client = MongoClient(host='localhost', port=27017)
print(f"client: {client}\n")

# удалить БД
# если такой БД нет, то ничего не произойдет
client.drop_database('test-database')

# получить (создать) БД
# ВНИМАНИЕ: в MongoDB БД не создается до тех пор пока нет нет контента
db = client['test-database']
print(f"db: {db}\n")

# получить (создать) коллекцию
# collection = db['test_collection']
collection = db.test_collection
print(f"collection: {collection}\n")
print(f"{'*' * num_sep}\n")

# ------Добавление------------------------------------------------------------------------------------------------------
one_post = {"_id": ObjectId("012345678901234567890123"),    # "_id": 555
            "author": "Mike",
            "text": "bla bla bla",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}

# добавить один документ и получить его id
insert_one_result = db.test_collection.insert_one(one_post)
print(f"db.test_collection.insert_one(one_post):\n"
      f"\ttype = {type(insert_one_result)}\n"
      f"\tvalue = {insert_one_result}\n")
one_post_id = insert_one_result.inserted_id
print(f"db.test_collection.insert_one(one_post).inserted_id:\n"
      f"\ttype = {type(one_post_id)}\n"
      f"\tvalue = {one_post_id}\n")

# DeprecationWarning: insert is deprecated. Use insert_one or insert_many instead
# post_id = db.test_collection.insert(one_post)
# print(f"insert(one_post).inserted_id: {post_id}\n")

print(f"{'-' * num_sep}\n")

# добавить несколько документов (bulk inserts)
many_posts = [{"author": "Ira",
               "text": "Cute cats!",
               "tags": ["bulk", "insert"],
               "date": datetime.datetime.utcnow()},
              {"author": "Misha",
               "title": "Craze stories about dogs",
               "tags": ["bulk", "insert"],
               "text": "bla bla bla",
               "date": datetime.datetime.utcnow()}]

insert_many_result = db.test_collection.insert_many(many_posts)
print(f"db.test_collection.insert_many(many_posts):\n"
      f"\ttype = {type(insert_many_result)}\n"
      f"\tvalue = {insert_many_result}\n")
many_post_ids = insert_many_result.inserted_ids
print(f"db.test_collection.insert_many(many_posts).inserted_ids:\n"
      f"\ttype = {type(many_post_ids)}\n"
      f"\tvalue = {many_post_ids}\n")

print(f"{'*' * num_sep}\n")
# ------Запросы---------------------------------------------------------------------------------------------------------

# получить имена коллекций из БД
print(f"db.list_collection_names(): {db.list_collection_names()}\n")

print(f"{'-' * num_sep}\n")

# получить один любой документ из коллекции
print(f"db.test_collection.find_one():\n{pprint.pformat(db.test_collection.find_one())}\n")

print(f"{'-' * num_sep}\n")

# получить все документы из коллекции + сортировка по дате
print("db.test_collection.find():")
for doc in db.test_collection.find().sort("date"):
    print(f"id: {doc['_id']}\tdate: {doc['date']}")
    # print(f"{pprint.pformat(doc)}\n")

print(f"{'-' * num_sep}\n")

# получить один документ из коллекции удовлетворяющий условию (такой существует)
print(f"db.test_collection.find_one({{'author': 'Mike'}}):\n"
      f"{pprint.pformat(db.test_collection.find_one({'author': 'Mike'}))}\n")

# получить один документ из коллекции удовлетворяющий условию (такого не существует)
print(f"db.test_collection.find_one({{'author': 'Eliot'}}): {db.test_collection.find_one({'author': 'Eliot'})}\n")

print(f"{'-' * num_sep}\n")

# получить все документы удовлетворяющие условию из коллекции
print("db.test_collection.find({{'author': 'Ira'}}):")
for doc in db.test_collection.find({'author': 'Ira'}):
    print(f"id: {doc['_id']}")
    # print(f"{pprint.pformat(doc)}\n")

print(f"{'-' * num_sep}\n")

# получить один документ по id из коллекции (такой существует)
# ВНИМАНИЕ: id должен быть типа bson.objectid.ObjectId
print(f"db.test_collection.find_one({{'_id': {one_post_id}}}):\n"
      f"{pprint.pformat(db.test_collection.find_one({'_id': one_post_id}))}\n")

# если id НЕ bson.objectid.ObjectId
# можно преобразовать строку bson.objectid.ObjectId(str_id)
print(f"db.test_collection.find_one({{'_id': str({one_post_id})}}): "
      f"{pprint.pformat(db.test_collection.find_one({'_id': str(one_post_id)}))}\n")

print(f"{'-' * num_sep}\n")

# количество документов в коллекции
print(f"db.test_collection.count_documents({{}}): {db.test_collection.count_documents({})}\n")

# количество документов удовлетворяющих условию в коллекции
print(f"db.test_collection.count_documents({{'tags': ['bulk']}}): "
      f"{db.test_collection.count_documents({'tags': ['bulk']})}\n")

# безотносительно порядка или других элементов в массиве используйте оператор $all
print(f"db.test_collection.count_documents({{'tags': {{'$all': ['bulk']}}}}): "
      f"{db.test_collection.count_documents({'tags': {'$all': ['bulk']}})}\n")

print(f"db.test_collection.count_documents({{'tags': ['bulk', 'insert']}}): "
      f"{db.test_collection.count_documents({'tags': ['bulk', 'insert']})}\n")

print(f"{'*' * num_sep}\n")
# ------Обновление------------------------------------------------------------------------------------------------------

# попытаться обновить один документ и получить количество обновленных (0 или 1)
update_one_result = db.test_collection.update_one({'author': 'Ira'}, {'$set': {'text': 'Cute frogs'}})
print(f"db.test_collection.update_one({{'author': 'Ira'}}, {{'$set': {{'text': 'Cute frogs'}}):\n"
      f"\ttype = {type(update_one_result)}\n"
      f"\tvalue = {update_one_result}\n")
one_matched_count = update_one_result.matched_count
print(f"db.test_collection.update_one({{'author': 'Ira'}}, {{'$set': {{'text': 'Cute frogs'}}).matched_count:\n"
      f"\ttype = {type(one_matched_count)}\n"
      f"\tvalue = {one_matched_count}\n")
one_modified_count = update_one_result.modified_count
print(f"db.test_collection.update_one({{'author': 'Ira'}}, {{'$set': {{'text': 'Cute frogs'}}).modified_count:\n"
      f"\ttype = {type(one_modified_count)}\n"
      f"\tvalue = {one_modified_count}\n")

update_one_result = db.test_collection.update_one({'author': 'Cat'}, {'$set': {'text': 'Cute frogs'}})
print(f"db.test_collection.update_one({{'author': 'Cat'}}, {{'$set': {{'text': 'Cute frogs'}}):\n"
      f"\ttype = {type(update_one_result)}\n"
      f"\tvalue = {update_one_result}\n")
one_matched_count = update_one_result.matched_count
print(f"db.test_collection.update_one({{'author': 'Cat'}}, {{'$set': {{'text': 'Cute frogs'}}).matched_count:\n"
      f"\ttype = {type(one_matched_count)}\n"
      f"\tvalue = {one_matched_count}\n")
one_modified_count = update_one_result.modified_count
print(f"db.test_collection.update_one({{'author': 'Cat'}}, {{'$set': {{'text': 'Cute frogs'}}).modified_count:\n"
      f"\ttype = {type(one_modified_count)}\n"
      f"\tvalue = {one_modified_count}\n")

print(f"{'-' * num_sep}\n")

# попытаться обновить все документы удовлетворяющие условию и получить количество обновленных
update_many_result = db.test_collection.update_many({'text': 'bla bla bla'}, {'$set': {'text': 'New cool text'}})
print(f"db.test_collection.update_many({{'text': 'bla bla bla'}}, {{'$set': {{'text': 'New cool text'}}):\n"
      f"\ttype = {type(update_many_result)}\n"
      f"\tvalue = {update_many_result}\n")
many_matched_count = update_many_result.matched_count
print(f"db.test_collection.update_many({{'text': 'bla bla bla'}}, "
      f"{{'$set': {{'text': 'New cool text'}}).matched_count:\n"
      f"\ttype = {type(many_matched_count)}\n"
      f"\tvalue = {many_matched_count}\n")
many_modified_count = update_many_result.modified_count
print(f"db.test_collection.update_many({{'text': 'bla bla bla'}}, "
      f"{{'$set': {{'text': 'New cool text'}}).modified_count:\n"
      f"\ttype = {type(many_modified_count)}\n"
      f"\tvalue = {many_modified_count}\n")


print(f"{'*' * num_sep}\n")
# ------Удаление--------------------------------------------------------------------------------------------------------

# попытаться удалить один документ и получить количество удаленных (0 или 1)
delete_one_result = db.test_collection.delete_one({'author': 'Ira'})
print(f"db.test_collection.delete_one({{'author': 'Ira'}}:\n"
      f"\ttype = {type(delete_one_result)}\n"
      f"\tvalue = {delete_one_result}\n")
one_deleted_count = delete_one_result.deleted_count
print(f"db.test_collection.delete_one({{'author': 'Ira'}}).deleted_count:\n"
      f"\ttype = {type(one_deleted_count)}\n"
      f"\tvalue = {one_deleted_count}\n")

delete_one_result = db.test_collection.delete_one({'author': 'Cat'})
print(f"db.test_collection.delete_one({{'author': 'Cat'}}:\n"
      f"\ttype = {type(delete_one_result)}\n"
      f"\tvalue = {delete_one_result}\n")
one_deleted_count = delete_one_result.deleted_count
print(f"db.test_collection.delete_one({{'author': 'Cat'}}).deleted_count:\n"
      f"\ttype = {type(one_deleted_count)}\n"
      f"\tvalue = {one_deleted_count}\n")

print(f"{'-' * num_sep}\n")

# попытаться удалить все документы удовлетворяющие условию и получить количество удаленных
delete_many_result = db.test_collection.delete_many({'text': {'$eq': 'bla bla bla'}})
print(f"db.test_collection.delete_many({{'text': {{'$eq': 'bla bla bla'}}}}:\n"
      f"\ttype = {type(delete_many_result)}\n"
      f"\tvalue = {delete_many_result}\n")
many_deleted_count = delete_many_result.deleted_count
print(f"db.test_collection.delete_many({{'text': {{'$eq': 'bla bla bla'}}}}.deleted_count:\n"
      f"\ttype = {type(many_deleted_count)}\n"
      f"\tvalue = {many_deleted_count}\n")

print(f"{'*' * num_sep}\n")
