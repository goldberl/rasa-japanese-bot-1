# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

class ActionCheckNumQuestions(Action):

    def name(self) -> Text:
        return "action_check_numQ"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        num_q = tracker.get_slot("quesAsked")
        print("\nNumQ from slot:　" + str(num_q))

        if num_q == None:
            num_q = 0
            num_q +=1
            dispatcher.utter_message(text="You asked " + str(num_q) + " questions")
            print("NumQ after adding 1:　" + str(num_q))

        elif num_q <5:
            num_q +=1
            dispatcher.utter_message(text="You asked " + str(num_q) + " questions")
            print("NumQ after adding 1:　" + str(num_q))

        else:
            print("User asked " + str(num_q))
            dispatcher.utter_message(text="You asked 6 questions. Goodbye.")


        return [SlotSet("quesAsked", num_q)]


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Sorry, can you rephrase that message?")

        # tell the user they are being passed to a customer service agent
        dispatcher.utter_message(text="I am passing you to a human...")

        # assume there's a function to call customer service
        # pass the tracker so that the agent has a record of the conversation between the user
        # and the bot for context
        call_customer_service(tracker)

        # pause the tracker so that the bot stops responding to user input
        return [ConversationPaused(), UserUtteranceReverted()]

# # class ActionDefaultFallback(Action):
#
#     def name(self):
#         return "action_default_ask_affirmation"
#
#     async def run(self, dispatcher, tracker, domain):
#         # select the top three intents from the tracker
#         # ignore the first one -- nlu fallback
#         predicted_intents = tracker.latest_message["intent_ranking"][1:4]
#
#         # A prompt asking the user to select an option
#         message = "Sorry! What do you want to do?"
#
#         # a mapping between intents and user friendly wordings
#         intent_mappings = {
#             "inform_name": "Tell me your name",
#             "greet": "Agree",
#             "goodbye": "End conversation"
#         }
#
#         # show the top three intents as buttons to the user
#         buttons = [
#             {
#                 "title": intent_mappings[intent['name']],
#                 "payload": "/{}".format(intent['name'])
#             }
#             for intent in predicted_intents
#         ]
#
#         # add a "none of these button", if the user doesn't
#         # agree when any suggestion
#         buttons.append({
#             "title": "None of These",
#             "payload": "/out_of_scope"
#         })
#         dispatcher.utter_message(text=message, buttons=buttons)
#         return []

# class ActionTest(Action):
#
#     def name(self) -> Text:
#         return "action_test"
#
#     def run(self, dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#
#         print("HELLO this is a test action")
#         return[]
