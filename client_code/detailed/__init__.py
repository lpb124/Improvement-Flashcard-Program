from ._anvil_designer import detailedTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..User import User

class detailed(detailedTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = properties['user']
    #self.drop_down_1.items = self.user.topics
    self.drop_down_1.items = [''] + list(self.user.topics)
    # self.topic_name = properties['self.item']
    # self.set_name = properties['self.set_item']
    # Any code you write here will run before the form opens.

  # def drop_down_1_change(self, **event_args):
  #   """This method is called when an item is selected"""
  #   self.drop_down_1.items = app_tables.user()
  # def drop_down_1_change(self, **event_args):
  #   """This method is called when an item is selected"""
  #   self.drop_down_1.items = self.userInstance.topics
  #   item = self.drop_down_1.selected_value 
  #   if selected_topic_name is not None:
  #     topic_row = app_tables.topics.get(name=selected_topic_name)
  #   if topic_row is not None:
  #     selected_set = topic_row['set']
  #     self.drop_down_2.items = [item['name'] for item in selected_set]
  #   if item is not None:
  #     self.label_2.visible = True
  #     self.drop_down_2.visible = True
  #   pass
  def drop_down_1_change(self, **event_args):
    #self.drop_down_1.items = self.userInstance.topics
    self.topic_item = self.drop_down_1.selected_value 
    
    if self.item is not None:
        topic_row = app_tables.topic.get(Name=self.topic_item)
        
        if topic_row is not None:
            selected_set = topic_row['Sets']
            self.drop_down_2.items = [''] + [self.item['Name'] for self.item in selected_set]
            
            self.label_2.visible = True
            self.drop_down_2.visible = True
    pass
  def drop_down_2_change(self, **event_args):
    """This method is called when an item is selected"""
    self.set_item = self.drop_down_2.selected_value
    print(self.set_item)
    if self.set_item is not None:
      self.flow_panel_1.visible = True
    
  
    pass

  def primary_color_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('hub')
    pass

  def primary_color_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.alert("You are already in the detailed set selector")
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('score_summary', user = self.user, set_name =self.set_item, topic_name = self.topic_item)    
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('session', user = self.user, set_name =self.set_item, topic_name = self.topic_item)    
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('flashcard_editor', user = self.user, set_name =self.set_item, topic_name = self.topic_item)  
    pass
