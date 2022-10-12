from pymongo import MongoClient
from msilib.schema import Error
import json

class DBRepository:
    
    def __init__(self, table):
        client = MongoClient("mongodb+srv://root:nMoiWNI9fZAvAEf2@cluster0.hif69ym.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database('Train_Bot')
        self.table = db[table]
    def insert(self,param):
        self.table.insert_one(param)
    def find(self,filter):
        return self.table.find_one(filter)
    def update(self,filter,param):
        return self.table.update_one(filter,param)   
#client = MongoClient("mongodb+srv://root:nMoiWNI9fZAvAEf2@cluster0.hif69ym.mongodb.net/?retryWrites=true&w=majority")
#db = client.get_database('Train_Bot')
#users = db.Users
#user = users.update_one({"name": "dasha"}, {'$push':{ 'questions': "lalala" }})
class BaseRepository:
    def __init__(self):
        self.items = DBRepository("Users")
    def findUser(self,name):
        text = "Ok, i remember"
        if(self.items.find({'name': name})):
            text = "Hello glad to see you again"
        else:
            self.items.insert({'name': name, 'questions': []})
        return text
    def addQuestions(self,name, question):
        self.items.update({"name": name}, {'$push':{ 'questions': question }})

    def findQuestions(self,name):
        user = self.items.find({"name": name})
        return list(user['questions'])


users = BaseRepository()
print(users.findQuestions("dasha"))




