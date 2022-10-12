from pymongo import MongoClient
from msilib.schema import Error
import json


client = MongoClient("mongodb+srv://root:nMoiWNI9fZAvAEf2@cluster0.hif69ym.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('Train_Bot')
users = db.Users
user = users.update_one({"name": "dasha"}, {'$push':{ 'questions': "lalala" }})
print(user['questions'])




