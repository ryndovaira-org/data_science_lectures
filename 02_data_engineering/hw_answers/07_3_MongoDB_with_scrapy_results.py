# -----Импорт пакетов-------------------------------------------------------------
import pprint

from pymongo import MongoClient
import json

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
collection = db.habr_news_collection
print(f"collection: {collection}\n")

# ------Добавление------------------------------------------------------------------------------------------------------

# загрузить json полученный в результате работы scrapy
with open('../lectures/scrapy_lecture_project/habr_news.json') as json_file:
    habr_news = json.load(json_file)

# добавить все данные из json в mongodb
insert_many_result = db.habr_news_collection.insert_many(habr_news)
print(f"db.habr_news_collection.insert_many(habr_news):\n"
      f"\ttype = {type(insert_many_result)}\n"
      f"\tvalue = {insert_many_result}\n")
many_post_ids = insert_many_result.inserted_ids
print(f"db.habr_news_collection.insert_many(habr_news).inserted_ids:\n"
      f"\ttype = {type(many_post_ids)}\n"
      f"\tvalue_count = {len(many_post_ids)}\n")

# ------Запросы---------------------------------------------------------------------------------------------------------

# количество документов в коллекции
print(f"db.habr_news_collection.count_documents({{}}): "
      f"{db.habr_news_collection.count_documents({})}\n")

# получить имена коллекций из БД
print(f"db.list_collection_names(): "
      f"{db.list_collection_names()}\n")

# получить один любой документ из коллекции
print(f"db.habr_news_collection.find_one():\n"
      f"{pprint.pformat(db.habr_news_collection.find_one())}\n")

print(f"db.habr_news_collection.find_one({{'news_id': 529690}}):\n"
      f"{pprint.pformat(db.habr_news_collection.find_one({'news_id': 529690}))}\n")

# получить все документы из коллекции удовлетворяющие условию {'comments_counter': 3} + сортировка по 'news_id'
for doc in db.habr_news_collection.find({'comments_counter': 3}).sort("news_id"):
    print(f"news_id: {doc['news_id']}\ttitle: {doc['title']}")

print('\n\n')

# получить все документы из коллекции удовлетворяющие условию {'author': 'avouner'}
for doc in db.habr_news_collection.find({'author': 'avouner'}):
    print(f"news_id: {doc['news_id']}\ttitle: {doc['title']}")

# получить количество документов из коллекции
# поле tags которых содержит `Научно-популярное` (другие теги тоже допустимы)
# безотносительно порядка или других элементов в массиве используйте оператор $all
print(f"db.habr_news_collection.count_documents({{'tags': {{'$all': ['Научно-популярное']}}}}): "
      f"{db.habr_news_collection.count_documents({'tags': {'$all': ['Научно-популярное']}})}\n")

# ------Обновление------------------------------------------------------------------------------------------------------

# установить в качестве `author` имя `MONGO` 
# во всех документах удовлетворяющие условию {'hubs': {'$all': ['Астрономия']}} 
# и получить количество обновленных
update_many_result = db.habr_news_collection.update_many({'hubs': {'$all': ['Астрономия']}}, 
                                                         {'$set': {'author': 'MONGO'}})
many_matched_count = update_many_result.matched_count
print(f"many_matched_count\ntype = {type(many_matched_count)}\n"
      f"value = {many_matched_count}\n")
many_modified_count = update_many_result.modified_count
print(f"many_modified_count\ntype = {type(many_modified_count)}\n"
      f"value = {many_modified_count}\n")

# получить количество документов из коллекции, в которых 'author' = 'MONGO'
print(f"db.habr_news_collection.count_documents({{'author': 'MONGO'}}): "
      f"{db.habr_news_collection.count_documents({'author': 'MONGO'})}")

# ------Удаление--------------------------------------------------------------------------------------------------------

# удалить все документы, у которых 'comments_counter' равен 0
# и получить количество удаленных
delete_many_result = db.habr_news_collection.delete_many({'comments_counter': 0})
print(f"delete_many_result:\n"
      f"\ttype = {type(delete_many_result)}\n"
      f"\tvalue = {delete_many_result}\n")
many_deleted_count = delete_many_result.deleted_count
print(f"many_deleted_count:\n"
      f"\ttype = {type(many_deleted_count)}\n"
      f"\tvalue = {many_deleted_count}\n")
