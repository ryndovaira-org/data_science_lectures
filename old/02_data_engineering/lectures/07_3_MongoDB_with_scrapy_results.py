# -----Импорт пакетов-------------------------------------------------------------
import json
import pprint

from pymongo import MongoClient

# -----Подключение----------------------------------------------------------------

# установить соединение с MongoClient
# MongoClient('mongodb://localhost:27017/')
client = MongoClient(host='localhost', port=27017)
print(f"client: {client}\n")

# удалить БД (каждый раз начинаем "с чистого листа")
# если такой БД нет, то ничего не произойдет
client.drop_database('habr')

# создать БД
# ВНИМАНИЕ: в MongoDB БД не создается до тех пор пока нет нет контента
db = client['habr']
print(f"db: {db}\n")

# создать коллекцию
collection = db.habr_companies_collection
print(f"collection: {collection}\n")

# ------Добавление------------------------------------------------------------------------------------------------------

# загрузить json полученный в результате работы scrapy
with open('./scrapy_lecture_project/habr_companies.json') as json_file:
    habr_news = json.load(json_file)

# добавить все данные из json в mongodb
insert_many_result = db.habr_companies_collection.insert_many(habr_news)
print(f"db.habr_companies_collection.insert_many(many_posts):\n"
      f"\ttype = {type(insert_many_result)}\n"
      f"\tvalue = {insert_many_result}\n")
many_post_ids = insert_many_result.inserted_ids
print(f"db.habr_companies_collection.insert_many(many_posts).inserted_ids:\n"
      f"\ttype = {type(many_post_ids)}\n"
      f"\tvalue_count = {len(many_post_ids)}\n")

# ------Запросы---------------------------------------------------------------------------------------------------------

# количество документов в коллекции
print(f"db.habr_companies_collection.count_documents({{}}): {db.habr_companies_collection.count_documents({})}\n")

# получить имена коллекций из БД
print(f"db.list_collection_names(): {db.list_collection_names()}\n")

# получить один любой документ из коллекции
print(f"db.habr_companies_collection.find_one():\n"
      f"{pprint.pformat(db.habr_companies_collection.find_one())}\n")

print(f"db.habr_companies_collection.find_one({{'name': Авито}}):\n"
      f"{pprint.pformat(db.habr_companies_collection.find_one({'name': 'Авито'}))}\n")

# получить все документы из коллекции удовлетворяющие условию {'counter_subscribers': 6} + сортировка по 'name'
print(f"db.habr_companies_collection.find({{'counter_subscribers': 6}}):")
for doc in db.habr_companies_collection.find({'counter_subscribers': 6}).sort("name"):
    print(f"name: {doc['name']}\tinfo: {doc['info']}")

# получить все документы из коллекции удовлетворяющие условию {'counter_subscribers': 9}
print(f"\ndb.habr_companies_collection.find({{'counter_subscribers': 9}}):")
for doc in db.habr_companies_collection.find({'counter_subscribers': 9}):
    print(f"name: {doc['name']}\tinfo: {doc['info']}")

# получить количество документов из коллекции поле tags которых содержит `Программирование` (другие теги тоже допустимы)
# безотносительно порядка или других элементов в массиве используйте оператор $all
print(f"\ndb.habr_companies_collection.count_documents({{'tags': {{'$all': ['Программирование']}}}}): "
      f"{db.habr_companies_collection.count_documents({'tags': {'$all': ['Программирование']}})}\n")

# ------Обновление------------------------------------------------------------------------------------------------------

# установить в качестве `name` имя `MONGO` 
# во всех документах удовлетворяющие условию {'tags': {'$all': ['Open source']}}
# и получить количество обновленных
update_many_result = db.habr_companies_collection.update_many({'tags': {'$all': ['Open source']}},
                                                              {'$set': {'name': 'MONGO'}})
print(f"\ndb.habr_companies_collection.update_many({{'tags': {{'$all': ['Open source']}}}},"
      f"{{'$set': {{'name': 'MONGO'}}}}:")
many_matched_count = update_many_result.matched_count
print(f"many_matched_count\ntype = {type(many_matched_count)}\n"
      f"value = {many_matched_count}\n")
many_modified_count = update_many_result.modified_count
print(f"many_modified_count\ntype = {type(many_modified_count)}\n"
      f"value = {many_modified_count}\n")

# получить количество документов из коллекции, в которых 'name' = 'MONGO'
print(f"db.habr_companies_collection.count_documents({{'name': 'MONGO'}}): "
      f"{db.habr_companies_collection.count_documents({'name': 'MONGO'})}")

# ------Удаление--------------------------------------------------------------------------------------------------------

# удалить все документы, у которых 'name' равен 'MONGO'
# и получить количество удаленных
delete_many_result = db.habr_companies_collection.delete_many({'name': 'MONGO'})
print(f"delete_many_result:\n"
      f"\ttype = {type(delete_many_result)}\n"
      f"\tvalue = {delete_many_result}\n")
many_deleted_count = delete_many_result.deleted_count
print(f"many_deleted_count:\n"
      f"\ttype = {type(many_deleted_count)}\n"
      f"\tvalue = {many_deleted_count}\n")
