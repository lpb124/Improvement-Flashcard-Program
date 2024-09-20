from ._anvil_designer import homepageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..User import User
from ..ObjectReconstructor import ObjectReconstructor

class homepage(homepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
   self.init_components(**properties)
    
    
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('hub')
    pass
