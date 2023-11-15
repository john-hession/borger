# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import sqlite3

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionBookAppointment(Action):
    def name(self) -> Text:
        return 'action_book_appointment'

    def run(self, dispatcher:CollectingDispatcher, tracker:Tracker, 
        domain:Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        conn = sqlite3.connect('../sqlite/reservations.db')
        cursor = conn.cursor()
        sql = "INSERT INTO reservations (date, time_start, time_end, table_id, reserved_under, nr_guests) VALUES (?, ?, ?, ?, ?, ?);"

        cursor.execute(sql,('bla', 'bla', 'bla', '1', tracker.get_slot('name'), tracker.get_slot('size')))
        
        conn.commit()
        conn.close()
        return[]