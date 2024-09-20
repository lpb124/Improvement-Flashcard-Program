from ._anvil_designer import hubTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..User import User
from ..ObjectReconstructor import ObjectReconstructor

class hub(hubTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.user = properties['user']
    # app_tables.definition.delete_all_rows()
    # app_tables.statistics.delete_all_rows()
    # app_tables.set.delete_all_rows()
    # app_tables.term.delete_all_rows()
    # app_tables.topic.delete_all_rows()
    # app_tables.user.delete_all_rows()
    # app_tables.id_manager_.delete_all_rows()
    # app_tables.flashcard_.delete_all_rows()

   #Checking if the user id is 0 which means that the program has never been used, if it is the user objected is is reconstucted 
    if app_tables.user.get(ID = 0):
      reconstructer = ObjectReconstructor()
      self.user = reconstructer.reconstruct_user(app_tables.user.get(ID = 0))
    else:
      self.user = User()
    #GEtting id row
    id_row = app_tables.id_manager_.get(Key = 'ID_manager')
    self.current_id = id_row['Set']
    self.current_id = self.current_id - 1

    #1 recent
  # First recent set
    self.first_recent = app_tables.set.get(ID=self.current_id)
    if self.first_recent is None or self.first_recent['Name'] is None:
        self.button_5.text = "Add a set first!"
    else:
        self.button_5.text = self.first_recent['Name']

# Second recent set
    self.second_recent = app_tables.set.get(ID=self.current_id - 1)
    if self.second_recent is None or self.second_recent['Name'] is None:
        self.button_2.text = "Add a set first!"
    else:
        self.button_2.text = self.second_recent['Name']
    
    # Third recent set
    self.third_recent = app_tables.set.get(ID=self.current_id - 2)
    if self.third_recent is None or self.third_recent['Name'] is None:
        self.button_3.text = "Add a set first!"
    else:
        self.button_3.text = self.third_recent['Name']
    
    # Fourth recent set
    self.fourth_recent = app_tables.set.get(ID=self.current_id - 3)
    if self.fourth_recent is None or self.fourth_recent['Name'] is None:
        self.button_4.text = "Add a set first!"
    else:
        self.button_4.text = self.fourth_recent['Name']
    
        # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('flashcard_creator_set',user = self.user)
    pass

  def primary_color_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('detailed', user = self.user)
    pass

  def primary_color_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.alert("You are already in the hub")
    pass

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    set_name = self.first_recent['Name']
    for topic in app_tables.topic.search():
        if topic['Sets']:
            for set_object in topic['Sets']:
                if set_object['Name'] == set_name:
                    open_form('session', user=self.user, set_name=set_name, topic_name=topic['Name'])
                    return  
    anvil.alert("No topic foundt")
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    set_name = self.second_recent['Name']
    for topic in app_tables.topic.search():
        if topic['Sets']:
            for set_object in topic['Sets']:
                if set_object['Name'] == set_name:
                    open_form('session', user=self.user, set_name=set_name, topic_name=topic['Name'])
                    return  
    anvil.alert("No topic found")
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    set_name = self.third_recent['Name']
    for topic in app_tables.topic.search():
        if topic['Sets']:
            for set_object in topic['Sets']:
                if set_object['Name'] == set_name:
                    open_form('session', user=self.user, set_name=set_name, topic_name=topic['Name'])
                    return  
    anvil.alert("No topic found")
    pass

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    set_name = self.fourth_recent['Name']
    for topic in app_tables.topic.search():
        if topic['Sets']:
            for set_object in topic['Sets']:
                if set_object['Name'] == set_name:
                    open_form('session', user=self.user, set_name=set_name, topic_name=topic['Name'])
                    return  
    anvil.alert("No topic found")
    pass




