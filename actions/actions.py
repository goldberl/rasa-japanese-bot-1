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
import smtplib

# Runs if bot does not understand user's input
class ActionDefaultAskAffirmation(Action):

    def name(self):
        return "action_default_ask_affirmation"

    async def run(self, dispatcher, tracker, domain):
        print("in ActionDefaultAskAffirmation!!!")
	
	# Last thing user typed
        lastOutput = tracker.latest_message['text']
        # Gets the user's last intent by extracting it from tracker dict
        lastUserIntentDictionary = tracker.latest_message['intent']
        lastUserIntent = list(lastUserIntentDictionary.values())[0]
        
	# Gets last output of bot (last question that bot asked user)
        for event in tracker.events:
            if (event.get("event") == "bot"):
                lastBotMessage = event.get("text")
        print(lastBotMessage)

	# Fallback for if user says "I don't know" to bot's question
        if 'inform_idk' in lastUserIntent and lastBotMessage == "おなまえは？":
            dispatcher.utter_message(text = 'なまえをしっていませんか？そうですか。(ｏ・_・)', image="https://media.tenor.com/-caxkmc867EAAAAC/mochi-cat.gif")
        elif 'inform_idk' in lastUserIntent and lastBotMessage == "つぎのしつもん：ごしゅっしんはどこですか。":
            dispatcher.utter_message(text = 'ごしゅっしんをしっていませんか？そうですか。(ｏ・_・)', image="https://media.tenor.com/-caxkmc867EAAAAC/mochi-cat.gif")
        elif 'inform_idk' in lastUserIntent and lastBotMessage == "つぎのしつもん：なんねんせいですか。":
            dispatcher.utter_message(text = 'なんねんせいかしっていませんか？そうですか。 (ｏ・_・)', image="https://media.tenor.com/-caxkmc867EAAAAC/mochi-cat.gif")
        elif 'inform_idk' in lastUserIntent and lastBotMessage == "つぎのしつもん：なんさいですか。":
            dispatcher.utter_message(text = 'なんさいかしっていませんか？そうですか。 (ｏ・_・)', image="https://media.tenor.com/-caxkmc867EAAAAC/mochi-cat.gif")
        elif 'inform_idk' in lastUserIntent and lastBotMessage == "さいごのしつもん：せんこうは？":
            dispatcher.utter_message(text = 'せんこうをしっていませんか？だいじょうぶですよ。(´･ᴗ･ ` )', image="https://media.tenor.com/VcSkBaf5NMcAAAAi/mochi-cat-chibi-cat.gif")
        # Fallback if user answers bot's last question, but bot doesn't understand
        # bot just takes user's output and sticks in in the response
        elif lastBotMessage == "おなまえは？":
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
            dispatcher.utter_message(text='いちねんせいです！(.❛ ᴗ ❛.)', image = "https://media.tenor.com/RXzUeIltPNwAAAAi/mochi-cat.gif")
        # fallback for if the bot doesn't understand the receipient's name for the email or the email address
        elif "Please type the name of the person you want to email." in lastBotMessage:
            dispatcher.utter_message('The person you want to email is ' + lastOutput)
            SlotSet("recipient", lastOutput)
        elif "Please enter the email address of the person you want to email." in lastBotMessage:
            dispatcher.utter_message('The email address is ' + lastOutput)
            SlotSet("email", lastOutput)
        # else
        else:
            dispatcher.utter_message(text="すみません、わかりません。 Sorry, I don't quite understand (,,>﹏<,,).", image = "https://media.tenor.com/-caxkmc867EAAAAC/mochi-cat.gif")

        print(lastUserIntent)
        
        return [FollowupAction("after_handle_did_not_understand_answer")]	

# Followup action from ActionDefaultAskAffirmation that
# generates the bot's next response        
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

        # Gets the user's last intent by extracting it from tracker dict
        lastUserIntentDictionary = tracker.latest_message['intent']
        lastUserIntent = list(lastUserIntentDictionary.values())[0]

	# Asks user for to ask bot a question
        # The lastBotMessage is coming from the ActionDefaultAskAffirmation
        # and these if/elif statements are checking what the bot last said
        # and using substrings of the last message to identify what the bot says next
        
        # Fallback for if user says "I don't know" to bot's question
        # user says "I don't know" to answer question - bot prompts user to ask next question 
        if 'inform_idk' in lastUserIntent and "なまえ" in lastBotMessage:
            dispatcher.utter_message(text = 'では、わたしの name をきいてください。')
        elif 'inform_idk' in lastUserIntent and "しゅっしん" in lastBotMessage:
            dispatcher.utter_message('では、わたしの hometown をきいてください。')
        elif 'inform_idk' in lastUserIntent and "ねんせい" in lastBotMessage:
            dispatcher.utter_message('では、わたしの school year をきいてください。')
        elif 'inform_idk' in lastUserIntent and "さい" in lastBotMessage:
            dispatcher.utter_message('では、わたしの age をきいてください。')
        elif 'inform_idk' in lastUserIntent and "せんこう" in lastBotMessage:
            dispatcher.utter_message('では、わたしの major をきいてください。')
        # Fallback if user answers bot's last question, but bot doesn't understand
        # user answers and bot prompts user to ask next question
        elif "なまえは" in lastBotMessage:
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
        # fallback for if the bot doesn't understand the receipient's name for the email or the email address
        elif "The person you want to email is" in lastBotMessage:
            dispatcher.utter_message('Great. Now we need their email.')
        elif "The email address is" in lastBotMessage:
            dispatcher.utter_message('Thank you for the information.')
        #else
        else:
            dispatcher.utter_message("I am a simple bot. Please try the following options:(1) Type こんにちは to restart the conversation OR (2)Ask me about my 'name', 'hometown', 'age', 'school year', or 'major'.")
        
        print(lastUserIntent)
        return [Restarted()]

#Create action to log conversation, each time called will capture last bot output and user response
class LogConversation(Action):
  
    def name(self) -> Text:
         # Name of the action
        return "log_conversation"
  
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
	#Try to log conversation
        conversation_log = tracker.get_slot("conversation_log")
        for event in tracker.events:
            if (event.get("event") == "bot"):
                lastBotMessage = "Bot message: " + event.get("text")
        print("Last user message: " + tracker.latest_message.get("text"))
        print("Last bot message: " + lastBotMessage)


        conversation_log = str(conversation_log) + "\nUser message: " + tracker.latest_message.get("text")  + "\n" + lastBotMessage 
        return [SlotSet("conversation_log", conversation_log)]


# Creating new class to send emails.
class ActionEmail(Action):
  
    def name(self) -> Text:
         # Name of the action
        return "action_email"
  
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Tracker message log
        #message_log = tracker.latest_message['text']
        conversation_log = str(tracker.get_slot("conversation_log"))        

        # Getting the data stored in the
        # slots and storing them in variables.
        # these are for the person RECIEVING the mail
        
        recipient = tracker.get_slot("recipient")
        email_id = tracker.get_slot("email")
        # recipient = "Leah"
        # email_id = "goldberl@dickinson.edu"
          
        # Code to send email
        # Creating connection using smtplib module
        s = smtplib.SMTP('localhost')
          
        # Making connection secured
        s.starttls() 
         
        # Authentication
        # s.login("goldberl@dickinson.edu")

        #First not utterance is "None" and couldn't figure out another way to get rid of it from the log.  Sorry.  Todd
        conversation_log = conversation_log.replace("None", "")
          
        # Message to be sent
        message = "Hello {} , \n\nThis is a demo message from the RASA Japanese chatbot! If you are seeing this, then the email function is working.\n\nRegards,\nThe Chatbot & The Programmer".format(recipient) + "\n\nPlease find the message log below: \n" + conversation_log
        
	# The email address below is the person who is SENDING the mail  
        # Sending the mail
        s.sendmail("ilovecats1205@gmail.com",email_id, message)
          
        # Closing the connection
        s.quit()

       
          
        # Confirmation message
        dispatcher.utter_message(text="Email has been sent.")
        return []
       

# not used currently
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

#class ActionRestart(Action):

#  def name(self) -> Text:
#      return "action_restart"

#  async def run(
#      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
#  ) -> List[Dict[Text, Any]]:

#      print("in ActionRestart")
#      return [...]


# class ActionTest(Action):
#
#     def name(self) -> Text:
#         return "action_test"
#
#     def run(self, dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         print("HELLO this is a test action")
#         return[]
