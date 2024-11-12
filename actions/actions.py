# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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
# actions.py

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.types import DomainDict

# # Sample book data
# book_data = {
#     "fiction": [
#         {"title": "To Kill a Mockingbird", "author": "Harper Lee", "description": "A novel about racism and injustice."},
#         {"title": "1984", "author": "George Orwell", "description": "A dystopian novel on government surveillance."}
#     ],
#     "mystery": [
#         {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "description": "A thriller about a journalist and a hacker."},
#         {"title": "Gone Girl", "author": "Gillian Flynn", "description": "A suspense novel about a disappearing wife."}
#     ]
# }

# class ActionBookRecommendation(Action):
#     def name(self) -> str:
#         return "action_book_recommendation"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: DomainDict) -> list:
#         genre = tracker.get_slot("genre")

#         if genre and genre.lower() in book_data:
#             recommendations = book_data[genre.lower()]
#             message = f"Here are some {genre} books I recommend:\n"
#             for book in recommendations:
#                 message += f"{book['title']} by {book['author']}: {book['description']}\n"
#             dispatcher.utter_message(text=message)
#         else:
#             dispatcher.utter_message(text="I'm sorry, I don't have recommendations for that genre right now.")

#         return []


    

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionRecommendBooks(Action):

    def name(self) -> Text:
        return "action_book_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        genre = tracker.get_slot('genre')
        author = tracker.get_slot('author')
        
        # Replace 'YOUR_API_KEY' with your actual Google Books API key
        api_key = "AIzaSyCtp7mmL8XH-Eu8Cg3ljwigrlLrErlQkvE"
        
        # Determine the query type based on available slot data
        if genre:
            query = f"subject:{genre}"
        elif author:
            query = f"inauthor:{author}"
        else:
            dispatcher.utter_message(text="Please specify a genre or an author for recommendations.")
            return []
        
        # Construct the API URL with the API key
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
        
        # Make the API request
        response = requests.get(url)
        books_data = response.json()
        
        # Extract book titles and authors from the API response
        book_recommendations = [
            f"{item['volumeInfo']['title']} by {item['volumeInfo'].get('authors', ['Unknown'])[0]}"
            for item in books_data.get('items', [])
        ]
        recommendations = ", ".join(book_recommendations) if book_recommendations else "Sorry, no books found for that genre or author."

        # Send the recommendations as a response to the user
        dispatcher.utter_message(text=f"Here are some books you might like: {recommendations}")
        
        return []


