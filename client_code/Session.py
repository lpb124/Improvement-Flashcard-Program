import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from DoublyLinkedList import DoublyLinkedList
from Set import Set

class Session:
    def __init__(self,set):
      # set default values for each attribute that needs to be ketp track of during the a flashcard review session 
     self.flashcards = set.get_flashcards()
     self.current = self.flashcards.head
     self.current_index = 0
     self.correct = 0
     self.incorrect = 0
     self.incorrect_flashcards = DoublyLinkedList() # keeps track of flashcards that were wrong 
     self.confidence_ratings = [] #Storing confidence ratings inside the array
     self.score = 0
     self.current_streak = 0
     self.longest_streak = 0
     self.average_confidence = 0 
     self.end_of_normal_session = False
     self.end_of_incorrect_session = False
     self.end_of_all_session = False
     self.incorrect_flashcard_session_active = False
     


    def next(self):
        # if we havent gone through all flashcards
        if self.current.data.done == False:

            if (self.current.data.get_correct() == False):
                self.incorrect_flashcards.insert_tail(self.current.data)
                #If the current flashcards current score is "Incorrect" that flashcard is added
                #to the tail of a new flashcard deck just for the incorrect flashcards
                self.incorrect += 1
                self.current_streak = 0
            else: #if correct
                self.correct += 1
                self.current_streak += 1
                if self.current_streak > self.longest_streak:
                    self.longest_streak = self.current_streak
                self.score += 1

            # confidence set regardless  of correct or not
            print(self.current_index)
            print(len(self.confidence_ratings))
            self.confidence_ratings.append( self.current.data.get_confidence())
            self.current.data.done = True # set done to true

        # IF NOT LAST FLASHCARD
        if (self.current.next != None):
            #Current Node (self.current) points to the next node
            self.current = self.current.next
            self.current_index += 1
           
        else:
          
            # handle end of flashcards
            self.average_confidence = sum(self.confidence_ratings) / len(self.confidence_ratings)
          
            self.end_of_normal_session = True
            

    def previous(self):
        # Will update the conf ratings/ score and streaks
        if ( self.current.prev != None):
          # Current node (Self.current) is pointing to previous node (self.current.prev)
            self.current = self.current.prev
            self.current_index -= 1
        else:
          # If there are no previous nodes an alert is raised for the user
            
            anvil.alert("There are no previous flashcards")


    def start_incorrect_flashcard_session(self):
        # method to review incorrect flashcards
        self.incorrect_flashcard_session = True
        self.incorrect_flashcard_session_active = True
        self.current = self.incorrect_flashcards.head
    def next_incorrect_flashcard(self):
        # method to review incorrect flashcards
        if (self.current.next != None):
            self.current = self.current.next
        else:
            # handle end of flashcards
            self.end_of_incorrect_session = True
            self.end_of_all_sessions = True
    def previous_incorrect_flashcard(self):
        # method to review previous  incorrect flashcard
        if ( self.current.prev != None): # if we are not at the head of linked list 
            self.current = self.current.prev # gets previous flashcarc
        else:
            return False
   # getter methods for attributes 
    def get_correct(self):
        return self.correct
    def get_incorrect(self):
        return self.incorrect
    def get_score(self):
        return self.score
    def get_current_streak(self):
        return self.current_streak

    def get_longest_streak(self):
        return self.longest_streak
    def get_average_confidence(self):
        return self.average_confidence
    def get_confidence_ratings(self):
        return self.confidence_ratings
    def get_incorrect_flashcard_session_active(self):
        return self.incorrect_flashcard_session_active

