# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import sqlite3

from typing import Text, List, Any, Dict, Optional, Action

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import dateutil.parser
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
    
class ValidateRestaurantForm(FormValidationAction):
	def name(self) -> Text:
		return "validate_restaurant_form"

	async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
		required_slots = ["time"] + slots_mapped_in_domain
		return required_slots
		
	async def extract_time(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
  ) -> Dict[Text, Any]:
		datetime = tracker.get_slot("time")
		if (datetime == None):
			return {}
		datetime_obj = dateutil.parser.parse(datetime)
		time = datetime_obj.strftime('%H:%M')
		return {"time": time}

	async def validate_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
		datetime = dateutil.parser.parse(slot_value)
		time = datetime.strftime('%H:%M')
		hours = datetime.strftime('%H')
		#print(time)
		if (int(hours) < 19 or int(hours) > 22):
			#print(hours)
			dispatcher.utter_message(text="Please enter a valid time. :(")
			return {"time": None}
		return {"time": time}