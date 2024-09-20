from ._anvil_designer import flashcard_editorTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Session import Session
from ..Set import Set
from ..Flashcard import Flashcard
from ..Term import Term
from ..Definition import Definition


class flashcard_editor(flashcard_editorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = properties['user']
    self.set_name = properties['set_name']
    self.topic_name = properties['topic_name']
    self.set = self.user.get_topics()[self.topic_name].get_set(self.set_name)
    set_row = app_tables.set.get(ID=self.set.id)
    self.selected_set = set_row['Flashcards']
    self.drop_down_1.items = [''] + [str(i + 1) for i in range(len(self.selected_set))]
    

    self.CardImage = None
    self.term_save = False
    self.def_save = False

    pass

    # Any code you write here will run before the form opens.
      
  def term_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box."""
    self.term_save = True  # Set term flag to true indicating that term has been entered
    print("Term saved:", self.term_save)  # Debugging output
    if self.term_save:  # Check if definition has also been saved
        self.button_1.visible = True
        print("Button visibility:", self.button_1.visible)  # Debugging output

  def definition_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box."""
    self.def_save = True  # Set definition flag to true indicating that definition has been entered
    print("Definition saved:", self.def_save)  # Debugging output
    if self.term_save:  # Check if term has also been saved
        self.button_1.visible = True
        print("Button visibility:", self.button_1.visible) 

  def file_loader_1_change(self, file, **event_args):
      """This method is called when a new file is loaded into this FileLoader"""
      self.CardImage = self.file_loader_1.file

  def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      if confirm("Once you remove a flashcard, all your statistics for this set will be reset. Do you want to proceed?"):
        image_url = self.CardImage if self.CardImage else " "
        term = Term(self.term_box.text, image_url=image_url)
        definition = Definition(self.definition_box.text)
        self.flashcard = Flashcard(term, definition)
        self.set.add_flashcard(self.flashcard)
        stat_row = app_tables.statistics.get(ID=self.set.id) 
        stat_row.update(
            Longest_streak=0, 
            Average_confidence=0,
            Total_incorrect=0,
            Total_correct=0,
            Average_score=0,
            Latest_longest_streak=0,
            Score_history=[],
            Highest_score=0,
            Confidence_history=[],
            Lowest_score=1000000000000,
            Total_sessions=0,
            Current_score=0
        )
        alert("Flashcard removed and statistics reset.")
      else:
           alert("No changes were made.")
  pass

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.selected_index = self.drop_down_1.selected_value
    self.selected_index = int(self.selected_index) - 1
    self.selected_flashcard = self.selected_set[self.selected_index]
    front_row = self.selected_flashcard['Front']
    back_row = self.selected_flashcard['Back']
    term_content = front_row['Content']
    def_content = back_row['Content']
    self.label_1.text = "Front of card: " + term_content
    self.label_2.text = "Front of card: " + def_content
    self.flashcard_object = self.set.get_flashcard_by_front_name(term_content)
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm("Once you remove a flashcard, all your statistics for this set will be reset. Do you want to proceed?"):
        self.set.remove_flashcard(self.flashcard_object)
        stat_row = app_tables.statistics.get(ID=self.set.id) 
        stat_row.update(
            Longest_streak=0, 
            Average_confidence=0,
            Total_incorrect=0,
            Total_correct=0,
            Average_score=0,
            Latest_longest_streak=0,
            Score_history=[],
            Highest_score=0,
            Confidence_history=[],
            Lowest_score=1000000000000,
            Total_sessions=0,
            Current_score=0
        )
        # Refresh the list of flashcards in the dropdown
        set_row = app_tables.set.get(ID=self.set.id)
        self.selected_set = set_row['Flashcards']
        self.drop_down_1.items = [''] + [str(i + 1) for i in range(len(self.selected_set))]
        alert("Flashcard removed and statistics reset.")
    else:
        alert("No changes were made.")
    pass

  def primary_color_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('hub')
    pass


