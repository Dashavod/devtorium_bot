
from msilib.schema import Error
from typing import Text, List, Any, Dict
from urllib import response

from rasa_sdk import Tracker, FormValidationAction,Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from pymongo import MongoClient

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
class CosmoRepository:
    def __init__(self):
        self.items = DBRepository("Solar_system")
    def findPlanet(self,name):
        planet = self.items.find({"Name": name})
        return planet['Distance']

class UserRepository:
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

def clean_name(name):
    return "".join([c for c in name if c.isalpha()])

users = UserRepository()
cosmo = CosmoRepository()

class ActionAddQuestions(Action):

    def name(self) -> Text:
        return "action_add_questions"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        first_name = tracker.get_slot("first_name")
        question = tracker.get_slot("user_question")
        users.addQuestions(first_name,question)
        dispatcher.utter_message(text=f"success add {question}")

        return SlotSet("user_question",None)

class ActionAskCosmoQuestion(Action):

    def name(self) -> Text:
        return "action_cosmo_question"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        planet = tracker.get_slot("planet")
        parametr = tracker.get_slot("parameter")
        if(planet == None):
            return dispatcher.utter_message(text=f"No planet {planet}")
        res = cosmo.findPlanet(planet)
        dispatcher.utter_message(text=f"Radius of {planet} is {res}000km")

        return {"planet": None}
   

class ActionCheckQuestions(Action):

    def name(self) -> Text:
        return "action_check_questions"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        first_name = tracker.get_slot("first_name")
        if( first_name == None ):
            dispatcher.utter_message(text="enter name")
            return {"first_name": first_name}
        res = users.findQuestions(first_name)
        dispatcher.utter_message(text=str(res))
        dispatcher.utter_message(text="We waiting to response, maybe you want to add new questions")

        return {"first_name": first_name}
    

class ActionCheckUser(Action):

    def name(self) -> Text:
        return "action_check_user"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        first_name = tracker.get_slot("first_name")
        res = users.findUser(first_name)
        dispatcher.utter_message(text=res)
        return {"first_name": first_name}
    

class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
        name = clean_name(slot_value)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"first_name": None}
        return {"first_name": name}