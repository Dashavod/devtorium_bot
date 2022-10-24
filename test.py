import pandas as pd
from pymongo import MongoClient
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
    def find_many(self,filter):
        items = self.table.find(filter)
        return list(items)

class CosmoRepository:
    def __init__(self):
        self.items = DBRepository("Solar_system")
    def findPlanet(self,name):
        planet = self.items.find({"Name": name})
        return planet
    def filterPlanet(self,filter):
        planets = self.items.find_many({"Orbits": filter})
        return planets
cosmo = CosmoRepository()

generalInfo = cosmo.findPlanet("Mars")
res = cosmo.filterPlanet("Mars")
print(f"Radius of Mars is {generalInfo['Distance']}000km")
print(f"Mars is {generalInfo}")
names = []
for i in res: names.append(i["Name"])
print(names)

first_operand = tracker.get_slot("first_operand")
second_operand = tracker.get_slot("second_operand")
firstInfo = cosmo.findPlanet(first_operand)
secondInfo = cosmo.findPlanet(second_operand)
if(abs(int(firstInfo['O_Period'])) > abs(int(secondInfo['O_Period']))):
    print(f"{first_operand} greater then {second_operand}")
    print(f"{first_operand} have {firstInfo['O_Period']} days\n {second_operand} have {secondInfo['O_Period']} days\n ")

# users = BaseRepository()
# print(users.findQuestions("dasha"))
# client = MongoClient("mongodb+srv://root:nMoiWNI9fZAvAEf2@cluster0.hif69ym.mongodb.net/?retryWrites=true&w=majority")
# db = client["Train_Bot"]
# coll = db["Solar_system"]
# data = pd.read_csv("solar.csv")
# payload = json.loads(data.to_json(orient='records'))
# coll.insert_many(payload)
# print(coll.count())




