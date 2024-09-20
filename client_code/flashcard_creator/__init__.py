from ._anvil_designer import flashcard_creatorTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server 
from ..Flashcard import Flashcard
from ..Term import Term
from ..Definition import Definition 
from ..User import User 

class flashcard_creator(flashcard_creatorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = properties['user']
    self.topic_name = properties['topic']
    self.set_name = properties['set_name']
    self.set = self.user.get_topics()[self.topic_name].get_set(self.set_name)
    self.term_save = False
    self.def_save = False
    self.button_1.visible = False
    self.next_card.visible = False
    self.CardImage = None
    self.card_count = 1


  def term_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    # IF THERE IS AN IMAGE - create with image - if not leave empty
    self.term_save = True 
    if (self.def_save):
      self.button_1.visible = True
      

  def definition_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.def_save = True
    if self.term_save:
      self.button_1.visible = True
    pass
    
  def group_creation_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.CardImage = self.file_loader_1.file
    
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    image_url = self.CardImage if self.CardImage else " "
    print(image_url)
    term = Term(self.term_box.text, image_url=image_url)
    definition = Definition(self.definition_box.text)
    self.flashcard = Flashcard(term, definition)
    self.set.add_flashcard(self.flashcard)
    self.set.flashcards.size
    self.set.flashcards.display()
    self.next_card.visible = True 
    self.button_2.visible = True
      

  def next_card_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.term_box.text = ""
    self.definition_box.text = ""
    self.file_loader_1.clear()
    self.card_count += 1
    self.card_number.text = "Flashcard number: " + str(self.card_count)
    self.term_save = False
    self.def_save = False
    self.button_1.visible = False
    self.button_2.visible = False
    self.next_card.visible = False 
    self.CardImage = " "
    
    
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('session', user = self.user, set_name =self.set_name, topic_name = self.topic_name)
  
        

    pass

  