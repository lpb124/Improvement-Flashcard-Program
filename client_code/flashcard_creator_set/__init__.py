from ._anvil_designer import flashcard_creator_setTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..Topic import Topic
from ..User import User

class flashcard_creator_set(flashcard_creator_setTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.userInstance = properties['user']
    self.topic_name = ""
    self.set_name = ""
    self.drop_down_1.items = self.userInstance.topics

    # Any code you write here will run before the form opens.

  def create_topic_textbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    topic_name = self.create_topic_textbox.text
    self.userInstance.create_topic(topic_name)
    anvil.alert(f"Your topic: {topic_name} has been entered.")
    self.create_topic_textbox.enabled = False
    self.topic_name = topic_name.lower()
    
    pass

  def text_box_2_pressed_enter(self, **event_args):
    #text_box_2 is a text box component from Anvil, I set an event to the GUI. 
    #so when a user presses enter in the text box the method is called an executed.
    set_name = self.text_box_2.text 
    #Set name is from the user pressing enter in te GUI.
    if not self.topic_name or self.topic_name not in self.userInstance.get_topics():
     anvil.alert("Please select an existing topic or create a new one before adding a set.")
    topic = self.userInstance.get_topics()[self.topic_name]
    #Getting the instance of the Topic class
    topic.create_set(set_name)
    #Using my defined method in the Topic class I call for a new set to be created in the topic
    anvil.alert(f"Your set: {set_name} has been entered.")
    self.text_box_2.enabled = False
    self.set_name = set_name
    


  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.topic_name = self.drop_down_1.selected_value
    if self.drop_down_1 is not None:
      self.create_topic_textbox.enabled = False
      
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('flashcard_creator', user = self.userInstance, topic = self.topic_name, set_name = self.set_name)

  def primary_color_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("hub")
    pass




