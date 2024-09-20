import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
# Interface super class - both types of cardface inherit from it ( def and term )

class CardFace: 
    #Superclass
    def __init__(self,content,id = -1):
      # Constructor with default id set to -1
        self.content = content 
        self.id = id 
    # Display method that needs to be overriden to by subclasses t
    def display(self):
        raise NotImplementedError("SubClass must implement abstract method")
    #Edit content method that needs to be overidden by subclasses
    def edit_content(self, new_content):
        raise NotImplementedError("SubClass must implement abstract method")

