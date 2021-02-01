# -----Импорт пакетов-------------------------------------------------------------
import pprint

from pymongo import MongoClient
import json

# -----Подключение----------------------------------------------------------------

# Установить соединение с MongoClient
# MongoClient('mongodb://localhost:27017/')
client = MongoClient(host='localhost', port=27017)
print(f"client: {client}\n")

# удалить БД
# если такой БД нет, то ничего не произойдет
client.drop_database('habr')

# получить (создать) БД
# ВНИМАНИЕ: в MongoDB БД не создается до тех пор пока нет нет контента
db = client['habr']
print(f"db: {db}\n")

# получить (создать) коллекцию
collection = db.habr_news_collection
print(f"collection: {collection}\n")

with open('./scrapy_lecture_project/habr_news.json') as json_file:
    habr_news = json.load(json_file)

# выгрузить все данные из json в mongodb
insert_many_result = db.habr_news_collection.insert_many(habr_news)
print(f"db.habr_news_collection.insert_many(many_posts):\n"
      f"\ttype = {type(insert_many_result)}\n"
      f"\tvalue = {insert_many_result}\n")
many_post_ids = insert_many_result.inserted_ids
print(f"db.habr_news_collection.insert_many(many_posts).inserted_ids:\n"
      f"\ttype = {type(many_post_ids)}\n"
      f"\tvalue_count = {len(many_post_ids)}\n")

# количество документов в коллекции
print(f"db.habr_news_collection.count_documents({{}}): {db.habr_news_collection.count_documents({})}\n")

# получить один любой документ из коллекции
print(f"db.test_collection.find_one():\n{pprint.pformat(db.habr_news_collection.find_one())}\n")
