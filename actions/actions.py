# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class Action_chaohoi(Action):

    def name(self) -> Text:
        return "action_chaohoi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        button = {
            "type": "phone_number",
            "title": "Call hotline",
            "payload": "1900588856"
        }

        button1 = {
            "type": "web_url",
            "url": "https://miai.vn",
            "title": "Website"
        }
        button2 = {
            "type": "postback",
            "title": "Need more?",
            "payload": "more"
        }
        ret_text = "Hi! You can contact us via below methods:"
        dispatcher.utter_message(text=ret_text, buttons=[
                                 button, button1, button2])

        return []
