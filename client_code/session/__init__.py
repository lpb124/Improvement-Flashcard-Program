from ._anvil_designer import sessionTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..Session import Session
from ..Statistics import Statistics

class session(sessionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = properties['user']
    self.set_name = properties['set_name']
    self.topic_name = properties['topic_name']
    print("Selected set name:", self.set_name)
    print("selected topic name:", self.topic_name)
    self.set = self.user.get_topics()[self.topic_name].get_set(self.set_name)
    self.session = Session(self.set)
    self.statistics = Statistics(self.set)
    self.back_data.text = self.session.current.data.get_back().display()
    self.Front_data.text = self.session.current.data.get_front().display()[0]
    self.slider_1.slider_min = 1
    self.slider_1.slider_max = 5
    image = self.session.current.data.get_front().display()[1] 
    if image == " ":
      self.image_1.visible = False
    else:
     self.image_1.source = image
    self.slider_1.level = 1
    self.check = 0
    print(self.set.statistics.id)

    
    # Any code you write here will run before the form opens.

  def check_box_1_change(self, **event_args):
    #self.session.current.data.set_correct(self.check_box_1.checked)
    self.correct = self.check_box_1.checked
    return(self.check_box_1.checked)

  def slider_1_change(self, level, **event_args):
    """This method is called when the slider is moved"""
  #  self.session.current.data.set_confidence(self.slider_1.level)
    self.label_2.text = "Confidence level: " + str(self.slider_1.level)
    self.confidence = self.slider_1.level
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""

    if not self.check == 1:
        anvil.alert("Please enter your scores and save first.")
        return  
    
    self.session.next()
    self.update_flashcard_display()
    # self.handle_session_end()
    self.back_data.text = self.session.current.data.get_back().display()
    self.Front_data.text = self.session.current.data.get_front().display()[0]

    if self.column_panel_2.visible:
        self.column_panel_2.visible = False
        self.column_panel_3.visible = True

    if self.session.end_of_normal_session:
        self.set.update_statistics(self.session)
        self.column_panel_4.visible = True
        self.column_panel_2.visible = False
        self.column_panel_3.visible = False
        self.primary_color_1.visible = False
        self.button_1.visible = False
        self.button_2.visible = False

    if self.check_box_1.checked:
      self.check_box_1.checked = False
    self.primary_color_2.enabled = True
    self.slider_1.level = 0
    self.check = 0
    
  def update_flashcard_display(self):
    """Updates the display for the current flashcard, including the image."""
    if self.session.current:
        front_display = self.session.current.data.get_front().display()
        back_display = self.session.current.data.get_back().display()

        self.Front_data.text = front_display[0] if front_display else ""
        self.back_data.text = back_display if back_display else ""

        # Handle image display
        image = front_display[1] if len(front_display) > 1 else None
        if image and image != " ":  # Check if the image exists
            self.image_1.source = image
            self.image_1.visible = True
        else:
            self.image_1.source = None
            self.image_1.visible = False

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.session.previous()
    self.update_flashcard_display()
    self.primary_color_2.enabled = False
    self.check = 1

  def primary_color_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.column_panel_3.visible:
      self.column_panel_3.visible = False
      self.column_panel_2.visible = True
    else:
        self.column_panel_3.visible = True
        self.column_panel_2.visible = False
    
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('hub')
    pass

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.session.start_incorrect_flashcard_session()
    front_display = self.session.current.data.get_front().display()
    back_display = self.session.current.data.get_back().display()
    self.Front_data.text = front_display[0] if front_display else ""
    self.back_data.text = back_display if back_display else ""
    if len(front_display) > 1 and front_display[1] and front_display[1] != " ":
        self.image_1.source = front_display[1]
        self.image_1.visible = True
    else:
        self.image_1.source = None
        self.image_1.visible = False

    # Visibility settings for other components
    self.column_panel_3.visible = True
    self.button_5.visible = True
    self.button_6.visible = True
    self.button_1.visible = False
    self.button_2.visible = False
    self.column_panel_4.visible = False
    self.primary_color_2.visible = False
    self.label_1.visible = False
    self.label_2.visible = False
    self.slider_1.visible = False
    self.primary_color_1.visible = True
    self.check_box_1.visible = False

  def handle_incorrect_session_end(self):
    """Handles actions to take when the session ends."""
    if self.session.end_of_incorrect_session:
      self.column_panel_4.visible = True
      self.column_panel_2.visible = False
      self.column_panel_3.visible = False
      self.button_4.visible = False
      self.button_6.visible = False
      self.button_5.visible = False
      self.button_1.visible = False
      self.button_2.visible = False
      
      

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    #self.session.previous()
    self.session.previous_incorrect_flashcard()
    self.update_flashcard_display()
    self.primary_color_2.enabled = False
    pass

  def button_5_click(self, **event_args):
    self.session.next_incorrect_flashcard()
    self.update_flashcard_display()

    if self.session.end_of_incorrect_session:
      self.column_panel_4.visible = True
      self.column_panel_2.visible = False
      self.column_panel_3.visible = False
      self.button_4.visible = False
      self.button_3.visible = False
      self.primary_color_1.visible = False
      self.button_7.visible = True
    pass

  def button_7_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('hub')
    pass
  
  def handle_session_end(self):
    """Handles actions to take when the session ends."""
    if self.session.end_of_normal_session:
        self.set.update_statistics(self.session)
        self.column_panel_4.visible = True
        self.column_panel_2.visible = False
        self.column_panel_3.visible = False

  def primary_color_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.correct = self.check_box_1.checked
    self.confidence = self.slider_1.level
    print("correct:", self.correct)
    print("confidence:", self.confidence)
    self.check = 1
    self.primary_color_2.enabled = False
    self.session.current.data.set_correct(self.correct)
    self.session.current.data.set_confidence(self.confidence)
    pass


    
