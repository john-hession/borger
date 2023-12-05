# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import sqlite3
import dateparser

n_tables = 14
max_guests_per_table = 8

# def get_nr_tables_needed(number_guests):
#  nr_tables_needed = math.ceil(number_guests/max_nr_guests_per_table)
#  print("number_guests: {0}, nr_tables_needed: {1}".format(number_guests, nr_tables_needed))
#  return nr_tables_needed

class CheckAvailability(Action):

    def name(self) -> Text:
        return "action_check_availability" #check on this

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('name') is None:
            return [SlotSet("next_slot_to_fill", 'name')]
        if tracker.get_slot('date') is None:
            return [SlotSet("next_slot_to_fill", 'date')]
        if tracker.get_slot('time') is None:
            return [SlotSet("next_slot_to_fill", 'time')]
        if tracker.get_slot('seats') is None:
            return [SlotSet("next_slot_to_fill", 'seats')]
        if tracker.get_slot('tabletype') is None:
            return [SlotSet("next_slot_to_fill", 'tabletype')]

        conn = sqlite3.connect('/Users/Ayush Jain/Documents/borger/sqlite/restaurant-20231203.db') 
        cursor = conn.cursor()

        sql = "SELECT * FROM reservations"
        cursor.execute(sql)
        records = cursor.fetchall()

        tableavailable = False
        dt_get = dateparser.parse(tracker.get_slot('date') + ' ' + tracker.get_slot('time'))
        reserved_tables = 0
        guests = int(tracker.get_slot('seats'))

        if guests > max_guests_per_table:
            print("Party size too big, sorry!")
            dispatcher.utter_message(text="Not tonight guys, too many people")
            return [SlotSet("avail", tableavailable), SlotSet("next_slot_to_fill", 'none')] 

        for row in records:
            date_time_booking = dateparser.parse(row[0])
            date_diff = date_time_booking - dt_get
            print(date_diff.total_seconds())
            if date_diff.total_seconds() > -5400 and date_diff.total_seconds() < 5400:
                reserved_tables += 1
        if n_tables - reserved_tables >= 1:
            tableavailable = True
            print("We have a table for you!")
        else:
            print("No table available, sorry!")
            dispatcher.utter_message(text="Not tonight guys, sorry")

        # Close connection
        conn.close()

        return [SlotSet("avail", tableavailable), SlotSet("next_slot_to_fill", 'none')]
    
class ActionBookAppointment(Action):

    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # change address to YOUR absolute path
        conn = sqlite3.connect('/Users/Ayush Jain/Documents/borger/sqlite/restaurant-20231203.db') 
        cursor = conn.cursor()

        date_time_string = tracker.get_slot('date') + ' ' + tracker.get_slot('time')
        date_time_formatted = dateparser.parse(date_time_string).strftime("%m/%d/%Y, %H:%M:%S")

        sql="INSERT INTO reservations (date, reserved_under, nr_guests) VALUES (?, ?, ?);"
        cursor.execute(sql,(date_time_formatted, tracker.get_slot('name'), tracker.get_slot('name')))
            # Commit your changes in the database
        conn.commit()

        # Close connection
        conn.close()

        return []