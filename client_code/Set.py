import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from DoublyLinkedList import DoublyLinkedList
from Statistics import Statistics
class Set:
    def __init__(self, name, reconstruct = False, id = -1):
      # setting attributes 
        self.name = name
        self.flashcards = DoublyLinkedList() #Flashcard stored as a doubly linked list
        self.history = [] # score histroy 
        self.id = id
        self.statistics = None
 
        if not reconstruct:  #create a row if set is not reconstructed from db 
          self.statistics = Statistics() # create a statistic object because it needs one as an attribute
          self.create_row_db()
        else:
          self.statistics = Statistics(reconstruct = True) # if reoncstruct is happening - reconstruct that stat object 
        
    #add a flashcard to the set 
    def add_flashcard(self,flashcard):
        self.flashcards.insert_tail(flashcard) # add it to linked list 
        flashcard_row = app_tables.flashcard_.get(ID = flashcard.id) # get the flashcard row associated to that flashcard object
        set_row = app_tables.set.get(ID = self.id) #get set row 
        if set_row['Flashcards'] == None: # if this is first flascard you are creating (must be init in this way )
          set_row['Flashcards'] = [flashcard_row]
        else: # if not first flashcard add it to row using this syntax 
          set_row['Flashcards'] += [flashcard_row]
          
          
    def remove_flashcard(self,flashcard):
      # remove flashcard 
        try:
          
            self.flashcards.remove(flashcard) # remove from linked list 
            set_row = app_tables.set.get(ID=self.id)
            set_row['Flashcards'] = [fc for fc in set_row['Flashcards'] if fc['ID'] != flashcard.get_id()] # remove flashcard from flashcard row
            return True # if all works return true 
        except ValueError: 
            return False #if there is a value error return false 
    
    def get_flashcard_by_front_name(self, flashcard_term): # search through flashcard list for a flashcard with specific term 
      normalized_term = flashcard_term.strip().lower() # make sure term isnt in caps or with extra spaces 
      current = self.flashcards.head
      while current: # go through linked list to checking if the term matches in the flashcard
          print(f"Checking: {current.data.front.content.lower()} against {normalized_term}") 
          if current.data.front.content.strip().lower() == normalized_term:
              return current.data # return the flashcard that matches the naem 
          current = current.next
      raise ValueError(f"Flashcard with term '{normalized_term}' not found.") # raise value error if no name matches 


    def create_row_db(self):
      # method for creating new row in database 
      # gets the row in the id manager table containing the latest unique id number for each object
      # set id 
        id_row = app_tables.id_manager_.get(Key = 'ID_manager')
        current_id = id_row['Set']
        self.id = current_id
        # get the appropriate stat row based on the stats id 
        stat_row = app_tables.statistics.get(ID = self.statistics.id)
        # creates row for set 
        app_tables.set.add_row(Name = self.name, Statistics = stat_row, ID = current_id)
      # update set id number 
        new_id = current_id + 1
        id_row.update(Set = new_id)

  # setter and getter methods 
    def update_statistics(self,session):
        self.statistics.update(session)

    def update_history(self,session):
        self.history.append(session)
    
    def get_flashcards(self):
        return self.flashcards

    def set_statistics(self,statistics):
      self.statistics = statistics

    def get_statistics(self):
      return self.statistics

    def how_many_cards(self):
      # method to count flashcard card numbers in the db 
      flashcard_row2 = app_tables.set.get(Name= self.name)
      
      flashcards2 = flashcard_row2['Flashcards']
      # Check if the 'Flashcards' column is not empty
      if flashcards2 is not None: # counts number of flashcards in row 
          flashcard_count = len(flashcards2)
          return flashcard_count 
      

  