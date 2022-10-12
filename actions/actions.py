
from msilib.schema import Error
from typing import Text, List, Any, Dict
from urllib import response

from rasa_sdk import Tracker, FormValidationAction,Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from pymongo import MongoClient

client = MongoClient("mongodb+srv://root:nMoiWNI9fZAvAEf2@cluster0.hif69ym.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('Train_Bot')
users = db.Users

def clean_name(name):
    return "".join([c for c in name if c.isalpha()])

def findUser(name):

    text = "Ok, i remember you"

    if(users.find_one({'name': name})):
        text = "Hello glad to see you again"
    else:
        users.insert_one({'name': name, 'questions': []})
    return text

def addQuestions(name, question):
    users.update_one({"name": name}, {'$push':{ 'questions': question }})

def findQuestions(name):

    user = users.find_one({"name": name})
    return user['questions']

class ActionAddQuestions(Action):

    def name(self) -> Text:
        return "action_add_questions"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        first_name = tracker.get_slot("first_name")
        question = tracker.get_slot("user_question")
        addQuestions(first_name,question)
        dispatcher.utter_message(text=f"success add {question}")

        return SlotSet("user_question",None)
    

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
        res = findQuestions(first_name)
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
        res = findUser(first_name)
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