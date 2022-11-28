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
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import Restarted


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

        # return[]
        return [SlotSet("quesAsked", num_q)]



class ActionDefaultAskAffirmation(Action):

    def name(self):
        return "action_default_ask_affirmation"

    async def run(self, dispatcher, tracker, domain):
        print("in ActionDefaultAskAffirmation!!!")
	
	# Last thing user typed
        lastOutput = tracker.latest_message['text']
        

	# Gets last output of bot (last question that bot asked user)
        for event in tracker.events:
            if (event.get("event") == "bot"):
                lastBotMessage = event.get("text")
        print(lastBotMessage)

	# Comments on user's last input
        if lastBotMessage == "おなまえは？":
            dispatcher.utter_message('なまえは' + lastOutput + 'さんですか？いいなまえですね。よろしくおねがいします。٩(◕‿◕)۶')
        elif lastBotMessage == "つぎのしつもん：ごしゅっしんはどこですか。":
            dispatcher.utter_message('わかりました。しゅっしんは' + lastOutput + 'ですね。')
        elif lastBotMessage == "つぎのしつもん：なんねんせいですか。":
            dispatcher.utter_message('だいがくの' + lastOutput + 'ねんせいですか？それはたのしいです。')
        elif lastBotMessage == "つぎのしつもん：なんさいですか。":
            dispatcher.utter_message('そうか、' + lastOutput + 'さいですね。')
        elif lastBotMessage == "さいごのしつもん：せんこうは？":
            dispatcher.utter_message('わかりました！せんこうは' + lastOutput + '。とてもおもしろいですね。')
        # Sometimes bot has confidence level below .5 when user asks what the school year is.
        # To remedy this, we are adding this 'elif' statement for the bot to respond to however
        # the user asks about the bot school year.
        elif "では、わたしの school year をきいてください。" in lastBotMessage:
            dispatcher.utter_message('いちねんせいです！(.❛ ᴗ ❛.)')
        else:
            dispatcher.utter_message('ActionDefaultAskAffirmation - This text should not appear. Please type こんにちは to restart the conversation.')
        
        return [FollowupAction("after_handle_did_not_understand_answer")]	
        
class AfterHandleDidNotUnderstandAnswer(Action):

    def name(self) -> Text:
        return "after_handle_did_not_understand_answer"

    def run(self, dispatcher, tracker, domain):
        print("in AfterHandleDidNotUnderstandAnswer")
        
        # dispatcher.utter_message('We bonked at the beginning, so do not have any valid slots I can use to make bot look smart.  Ohe well.  Let us just resume the story with student asking bot a question.')

        # Gets last output of bot (based on dispatcher.utter_message from ActionDefaultAskAffirmation)
        for event in tracker.events:
            if (event.get("event") == "bot"):
                lastBotMessage = event.get("text")
        print(lastBotMessage)

	# Asks user for to ask bot a question
        # The lastBotMessage is coming from the ActionDefaultAskAffirmation
        # and these if/elif statements are checking what the bot last said
        # and using substrings of the last message to identify what the bot says next
        if "なまえは" in lastBotMessage:
            dispatcher.utter_message('では、わたしの name をきいてください。')
        elif "しゅっしんは" in lastBotMessage:
            dispatcher.utter_message('では、わたしの hometown をきいてください。')
        # Sometimes bot has confidence level below .5 when user asks what the school year is.
        # To remedy this, we are adding this 'elif' statement for the bot to respond to however
        # the user asks about the bot school year. The next question for the bot to ask is AGE.
        elif "いちねんせいです！(.❛ ᴗ ❛.)" in lastBotMessage:
            dispatcher.utter_message('つぎのしつもん：なんさいですか。')
        elif "ねんせい" in lastBotMessage:
            dispatcher.utter_message('では、わたしの school year をきいてください。')
        elif "さい" in lastBotMessage:
            dispatcher.utter_message('では、わたしの age をきいてください。')
        elif "せんこう" in lastBotMessage:
            dispatcher.utter_message('では、わたしの major をきいてください。')
        else:
            dispatcher.utter_message('AfterHandleDidNotUnderstandAnswer - This text should not appear. Please type こんにちは to restart the conversation.')
        
        
        return [Restarted()]       


#class ActionDefaultFallback(Action):
#    """Executes the fallback action and goes back to the previous state
#    of the dialogue"""
#
#    def name(self) -> Text:
#        return "action_default_fallback"
#
#    async def run(
#        self,
#        dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: Dict[Text, Any],
#    ) -> List[Dict[Text, Any]]:
#        dispatcher.utter_message("Sorry, can you rephrase that message?")
#        print("We are rewriting the action default fallback")
#
#	#  Revert user message which led to fallback.
#        return [FollowupAction("action_follow_up_new_story")]


#class ActionStartNewStory(Action):

#    def name(self):
#        return "action_start_new_story"

#    async def run(self, dispatcher, tracker, domain):
#        print("in ActionStartNewStory")
#        return [FollowupAction("action_follow_up_new_story")]


#class ActionFollowUpNewStory(Action):

#    def name(self) -> Text:
#        return "action_follow_up_new_story"

#    def run(self, dispatcher, tracker, domain):
#        print("in ActionFollowUpNewStory")
#        return []

#class ActionRestart(Action):

#  def name(self) -> Text:
#      return "action_restart"

#  async def run(
#      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
#  ) -> List[Dict[Text, Any]]:

#      print("in ActionRestart")

#      return [...]





#class ActionTest(Action):

#    def name(self) -> Text:
#        return "action_test"

#    def run(self, dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#        print("We made it out of the CUSTOM ACTION!")
#        return[]



# # We will catch NLU uncertainty here and override their function.
# class ActionDefaultAskAffirmation(Action):
#
#     def name(self):
#         return "action_default_ask_affirmation"
#
#
#     async def run(self, dispatcher, tracker, domain):
#
#         print('In ActionDefaultAskAffirmation!!')
#         story = tracker.get_slot('story')
#         hometown = tracker.get_slot('hometown')
#         lastOutput = tracker.latest_message['text']
#
#         # We will start each story with an action that sets
#         # the story slot so we know which conversation the user is having.
#
#         if story == 'trip' and hometown is None:
#         #print("message is " + tracker.latest_message['text'], "text2")
#
#         #Lets just say they’re in New York
#             return [SlotSet("hometown", "New York"), FollowupAction("after_handle_no_trip_location")]
#
#         else:
#             print("We are in default ask affirmation action and have not handled this scenario")
#             return []
#
#
# class AfterHandleNoTripLocation(Action):
#
#     def name(self) -> Text:
#         return "after_handle_no_trip_location"
#
#     def run(self, dispatcher, tracker, domain):
#         return []

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
