import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from CardFace import CardFace
class Flashcard:
  # this class is a flashcard class which contains 2 cardfaces, and it stores the confidence level and whether a user got that card correct during a session 
    def __init__(self, front, back, reconstruct = False, id = -1):
        # composite data structure - attributes of class are other classes (front and back )
        self.front = front # front is usually a term 
        self.back = back # back will usually be a definition 
        self.correct = 0 # 0 false 1 is true 
        self.confidence = -1 # default set confidence level to -1 
        self.state = 0 # 0 for front 1 for back
        self.done = False 
        self.id = id
        if not reconstruct: # if not reconsturcting object from db create a row for object 
          self.create_row_db()

    def flip(self): # flip between front and back of card 
        self.state = 1 - self.state
  
    def set_confidence(self,confidence): #set confidence
        if (self.done): # only able to set convidence if done is not set to true (that is they havent already reviewed that card )
            return False

        self.confidence = confidence
        return True
        

    def set_correct(self,correct):
        if (self.done): # cant set correct if card is already been reviewed 
            return False
        # set card result 
        if correct is True:
         self.correct = 1
        if correct is False:
          self.correct = 0 
        
        #self.correct = correct
        return True
    # getter methods 
    def get_front(self):
        return self.front
    
    def get_back(self):
        return self.back
    
    def get_confidence(self):
        return self.confidence
    
    def get_correct(self):
        return self.correct

  # setter methods for editing front and back content 
    def edit_front(self,new_front_text):
        self.front.edit_content(new_front_text)

    def edit_back(self,new_back_text):
        self.back.edit_content(new_back_text)


    def display(self): # display (or really return content ) based on the card state 
        if self.state == 0:
            return self.front.display()
        else:
            return self.back.display()

    def get_id(self): # getter for id 
      return self.id
    
    def create_row_db(self):
       # method for creating new row in database 
      # gets the row in the id manager table containing the latest unique id number for each object
      # set id 
        id_row = app_tables.id_manager_.get(Key = 'ID_manager')
        current_id = id_row['Flashcard']
        self.id = current_id

      # get front row for the front object get row associated to back object a
        front_row = app_tables.term.get(ID = self.front.id)
        back_row = app_tables.definition.get(ID = self.back.id)
        # add row to db 
        app_tables.flashcard_.add_row(Front = front_row, Back = back_row, ID = current_id)

      #update id manager with new id 
        new_id = current_id + 1
        id_row.update(Flashcard = new_id)

        

    def __str__(self):
      # to string method to nicely display flashcard textually 
        return f"(Front: {self.front.display()} back: {self.back.display()[:20]}...)"   

